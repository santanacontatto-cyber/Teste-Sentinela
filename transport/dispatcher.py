from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
RESULT_MARKER = "SENTINELA_RESULT_V1="
READ_OPS = {"health", "fs_read", "fs_search", "process_list", "broker_get", "profile_run"}
WRITE_OPS = {"fs_write_new", "fs_patch_cas"}
ALL_OPS = READ_OPS | WRITE_OPS
MAX_STEPS = 64
MAX_WORKERS = 8
MAX_FILE_BYTES = 65536
MAX_SEARCH_FILES = 2000
MAX_SEARCH_MATCHES = 200
MAX_BROKER_BYTES = 131072
BROKER_BASE = "http://127.0.0.1:47662"
MISSION_ID_RE = re.compile(r"^[A-Za-z0-9_.:-]{8,128}$")
STEP_ID_RE = re.compile(r"^[A-Za-z0-9_.:-]{1,64}$")

DEFAULT_ALLOWED_ROOTS = [
    Path(r"G:\Meu Drive\Sentinela_PC_Bridge"),
    Path(os.environ.get("LOCALAPPDATA", r"C:\Users\Administrador\AppData\Local")) / "Sentinela_Shadow",
]
DEFAULT_STATE_ROOT = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / "Sentinela_Transport"

PROFILE_MAP = {
    "orientation_suite": [sys.executable, r"G:\Meu Drive\Sentinela_PC_Bridge\shadow\run_orientation_shadow_suite.py"],
    "query_state_summary": [sys.executable, r"G:\Meu Drive\Sentinela_PC_Bridge\tools\query_state_summary.py"],
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _json_hash(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _parse_rfc3339(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        raise ValueError("expires_at must include timezone")
    return dt.astimezone(timezone.utc)


class MissionError(RuntimeError):
    pass


class ReceiptLedger:
    def __init__(self, path: Path):
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _connect(self) -> sqlite3.Connection:
        con = sqlite3.connect(self.path, timeout=30, isolation_level=None)
        con.execute("PRAGMA journal_mode=WAL")
        con.execute("PRAGMA busy_timeout=30000")
        return con

    def _init(self) -> None:
        with self._connect() as con:
            con.execute(
                """CREATE TABLE IF NOT EXISTS effects(
                   effect_key TEXT PRIMARY KEY,
                   intent_hash TEXT NOT NULL,
                   mission_id TEXT NOT NULL,
                   step_id TEXT NOT NULL,
                   status TEXT NOT NULL,
                   result_json TEXT,
                   created_at REAL NOT NULL,
                   updated_at REAL NOT NULL)"""
            )

    def begin(self, effect_key: str, intent_hash: str, mission_id: str, step_id: str) -> dict[str, Any]:
        now = time.time()
        with self._connect() as con:
            con.execute("BEGIN IMMEDIATE")
            row = con.execute(
                "SELECT intent_hash,status,result_json FROM effects WHERE effect_key=?", (effect_key,)
            ).fetchone()
            if row:
                if row[0] != intent_hash:
                    raise MissionError("effect_key already exists with different intent")
                result = json.loads(row[2]) if row[2] else None
                con.execute("COMMIT")
                return {"existing": True, "status": row[1], "result": result}
            con.execute(
                "INSERT INTO effects VALUES(?,?,?,?,?,?,?,?)",
                (effect_key, intent_hash, mission_id, step_id, "PENDING", None, now, now),
            )
            con.execute("COMMIT")
            return {"existing": False, "status": "PENDING", "result": None}

    def complete(self, effect_key: str, result: dict[str, Any]) -> None:
        with self._connect() as con:
            con.execute(
                "UPDATE effects SET status='COMPLETE',result_json=?,updated_at=? WHERE effect_key=?",
                (json.dumps(result, ensure_ascii=False, separators=(",", ":")), time.time(), effect_key),
            )


class ResourceLock:
    def __init__(self, lock_root: Path, resource: str, timeout: float = 30.0, stale_after: float = 300.0):
        self.lock_root = lock_root
        self.resource = resource
        self.timeout = timeout
        self.stale_after = stale_after
        self.path = lock_root / (hashlib.sha256(resource.encode("utf-8")).hexdigest() + ".lock")

    def __enter__(self):
        self.lock_root.mkdir(parents=True, exist_ok=True)
        deadline = time.time() + self.timeout
        while True:
            try:
                self.path.mkdir()
                (self.path / "owner.json").write_text(
                    json.dumps({"pid": os.getpid(), "created_at": time.time(), "resource": self.resource}),
                    encoding="utf-8",
                )
                return self
            except FileExistsError:
                try:
                    age = time.time() - self.path.stat().st_mtime
                    if age > self.stale_after:
                        for child in self.path.iterdir():
                            child.unlink(missing_ok=True)
                        self.path.rmdir()
                        continue
                except OSError:
                    pass
                if time.time() >= deadline:
                    raise MissionError("resource lock timeout")
                time.sleep(0.1)

    def __exit__(self, exc_type, exc, tb):
        try:
            for child in self.path.iterdir():
                child.unlink(missing_ok=True)
            self.path.rmdir()
        except OSError:
            pass


class Dispatcher:
    def __init__(
        self,
        allowed_roots: list[Path] | None = None,
        state_root: Path | None = None,
        max_workers: int = MAX_WORKERS,
    ):
        self.allowed_roots = [Path(p).resolve() for p in (allowed_roots or DEFAULT_ALLOWED_ROOTS)]
        self.state_root = (state_root or DEFAULT_STATE_ROOT).resolve()
        self.max_workers = max(1, min(int(max_workers), MAX_WORKERS))
        self.ledger = ReceiptLedger(self.state_root / "receipts.sqlite")
        self.lock_root = self.state_root / "locks"

    def _allowed_path(self, raw: str) -> Path:
        if not isinstance(raw, str) or not raw.strip():
            raise MissionError("path is required")
        p = Path(raw).expanduser().resolve()
        for root in self.allowed_roots:
            try:
                if os.path.commonpath([str(p), str(root)]) == str(root):
                    return p
            except ValueError:
                continue
        raise MissionError("path outside allowed roots")

    def _validate(self, mission: dict[str, Any]) -> None:
        if mission.get("version") != SCHEMA_VERSION:
            raise MissionError("unsupported mission version")
        mid = mission.get("mission_id")
        if not isinstance(mid, str) or not MISSION_ID_RE.fullmatch(mid):
            raise MissionError("invalid mission_id")
        wf = mission.get("workframe_id")
        if not isinstance(wf, str) or not wf.strip():
            raise MissionError("workframe_id is required")
        if mission.get("instruction_authority", "NONE") != "NONE":
            raise MissionError("instruction_authority must be NONE")
        mode = mission.get("mode", "read_only")
        if mode not in {"read_only", "controlled_write"}:
            raise MissionError("invalid mode")
        expires = mission.get("expires_at")
        if expires and _parse_rfc3339(expires) <= datetime.now(timezone.utc):
            raise MissionError("mission expired")
        steps = mission.get("steps")
        if not isinstance(steps, list) or not (1 <= len(steps) <= MAX_STEPS):
            raise MissionError("mission must contain 1..64 steps")
        ids = set()
        for step in steps:
            sid = step.get("id")
            op = step.get("op")
            if not isinstance(sid, str) or not STEP_ID_RE.fullmatch(sid) or sid in ids:
                raise MissionError("invalid or duplicate step id")
            ids.add(sid)
            if op not in ALL_OPS:
                raise MissionError(f"unsupported operation: {op}")
            deps = step.get("depends_on", [])
            if not isinstance(deps, list) or any(not isinstance(x, str) for x in deps):
                raise MissionError("depends_on must be a list of step ids")
            if op in WRITE_OPS:
                if mode != "controlled_write":
                    raise MissionError("write operation requires controlled_write mode")
                if not step.get("effect_key"):
                    raise MissionError("write operation requires effect_key")
        for step in steps:
            if any(dep not in ids for dep in step.get("depends_on", [])):
                raise MissionError("dependency references unknown step")

    def run(self, mission: dict[str, Any]) -> dict[str, Any]:
        started = time.time()
        self._validate(mission)
        steps = {s["id"]: s for s in mission["steps"]}
        pending = set(steps)
        results: dict[str, dict[str, Any]] = {}
        while pending:
            skipped = []
            for sid in list(pending):
                deps = steps[sid].get("depends_on", [])
                if any(results.get(d, {}).get("status") not in {"SUCCESS", "CACHED"} for d in deps if d in results):
                    if all(d in results for d in deps):
                        results[sid] = {"status": "SKIPPED_DEPENDENCY"}
                        pending.remove(sid)
                        skipped.append(sid)
            if not pending:
                break
            ready = [
                sid for sid in pending
                if all(dep in results for dep in steps[sid].get("depends_on", []))
            ]
            if not ready:
                if skipped:
                    continue
                raise MissionError("dependency cycle detected")
            with ThreadPoolExecutor(max_workers=min(self.max_workers, len(ready))) as pool:
                futures = {pool.submit(self._run_step, mission, steps[sid]): sid for sid in ready}
                for fut in as_completed(futures):
                    sid = futures[fut]
                    try:
                        results[sid] = fut.result()
                    except Exception as exc:
                        results[sid] = {"status": "ERROR", "error": f"{type(exc).__name__}: {exc}"}
                    pending.remove(sid)
        statuses = [r["status"] for r in results.values()]
        overall = "SUCCESS" if all(s in {"SUCCESS", "CACHED"} for s in statuses) else "ERROR"
        return {
            "schema": "sentinela-mission-receipt/1",
            "mission_id": mission["mission_id"],
            "workframe_id": mission["workframe_id"],
            "status": overall,
            "started_at": datetime.fromtimestamp(started, timezone.utc).isoformat().replace("+00:00", "Z"),
            "finished_at": _utc_now(),
            "duration_ms": int((time.time() - started) * 1000),
            "steps": results,
            "instruction_authority": "NONE",
        }

    def _run_step(self, mission: dict[str, Any], step: dict[str, Any]) -> dict[str, Any]:
        op = step["op"]
        if op in WRITE_OPS:
            return self._run_write(mission, step)
        return {"status": "SUCCESS", "data": self._execute_read(op, step.get("args") or {})}

    def _execute_read(self, op: str, args: dict[str, Any]) -> Any:
        if op == "health":
            return {"ok": True, "time": _utc_now(), "pid": os.getpid(), "workers": self.max_workers}
        if op == "fs_read":
            path = self._allowed_path(args["path"])
            max_bytes = min(int(args.get("max_bytes", MAX_FILE_BYTES)), MAX_FILE_BYTES)
            data = path.read_bytes()
            chunk = data[:max_bytes]
            return {
                "path": str(path), "size": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                "truncated": len(data) > max_bytes, "text": chunk.decode(args.get("encoding", "utf-8"), errors="replace"),
            }
        if op == "fs_search":
            root = self._allowed_path(args["root"])
            if not root.is_dir():
                raise MissionError("search root is not a directory")
            query = str(args.get("query", ""))
            pattern = str(args.get("pattern", "*"))
            use_regex = bool(args.get("regex", False))
            rx = re.compile(query, re.IGNORECASE) if use_regex else None
            matches, scanned = [], 0
            for path in root.rglob(pattern):
                if not path.is_file():
                    continue
                scanned += 1
                if scanned > MAX_SEARCH_FILES or len(matches) >= MAX_SEARCH_MATCHES:
                    break
                try:
                    if path.stat().st_size > 2 * 1024 * 1024:
                        continue
                    text = path.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                for lineno, line in enumerate(text.splitlines(), 1):
                    ok = bool(rx.search(line)) if rx else query.casefold() in line.casefold()
                    if ok:
                        matches.append({"path": str(path), "line": lineno, "text": line[:500]})
                        if len(matches) >= MAX_SEARCH_MATCHES:
                            break
            return {"root": str(root), "scanned_files": scanned, "matches": matches, "truncated": scanned > MAX_SEARCH_FILES or len(matches) >= MAX_SEARCH_MATCHES}
        if op == "process_list":
            if os.name == "nt":
                p = subprocess.run(["tasklist", "/fo", "csv", "/nh"], capture_output=True, text=True, timeout=15)
                rows = list(csv.reader(p.stdout.splitlines()))
                return [{"image": r[0], "pid": r[1], "memory": r[4]} for r in rows[:300] if len(r) >= 5]
            p = subprocess.run(["ps", "-eo", "pid,comm"], capture_output=True, text=True, timeout=15)
            return p.stdout.splitlines()[:300]
        if op == "broker_get":
            path = str(args.get("path", "/"))
            if not re.fullmatch(r"/[A-Za-z0-9_./?=&%:-]{0,220}", path):
                raise MissionError("invalid broker path")
            req = urllib.request.Request(BROKER_BASE + path, method="GET", headers={"User-Agent": "Sentinela-Transport/1"})
            try:
                with urllib.request.urlopen(req, timeout=min(float(args.get("timeout", 5)), 10.0)) as r:
                    body = r.read(MAX_BROKER_BYTES + 1)
                    return {"status": r.status, "truncated": len(body) > MAX_BROKER_BYTES, "body": body[:MAX_BROKER_BYTES].decode("utf-8", errors="replace")}
            except urllib.error.HTTPError as e:
                body = e.read(MAX_BROKER_BYTES)
                return {"status": e.code, "body": body.decode("utf-8", errors="replace")}
        if op == "profile_run":
            name = str(args.get("name", ""))
            command = PROFILE_MAP.get(name)
            if not command:
                raise MissionError("unknown profile")
            timeout = min(int(args.get("timeout_seconds", 180)), 180)
            p = subprocess.run(command, capture_output=True, text=True, timeout=timeout, cwd=str(Path(command[1]).parent))
            return {"profile": name, "exit_code": p.returncode, "stdout": p.stdout[-65536:], "stderr": p.stderr[-32768:]}
        raise MissionError("unknown read operation")

    def _run_write(self, mission: dict[str, Any], step: dict[str, Any]) -> dict[str, Any]:
        op = step["op"]
        args = step.get("args") or {}
        effect_key = str(step["effect_key"])
        intent = {"op": op, "args": args, "resource": step.get("resource")}
        intent_hash = _json_hash(intent)
        begin = self.ledger.begin(effect_key, intent_hash, mission["mission_id"], step["id"])
        if begin["status"] == "COMPLETE":
            return {"status": "CACHED", "data": begin["result"]}
        path = self._allowed_path(args["path"])
        resource = str(step.get("resource") or ("file://" + str(path)))
        with ResourceLock(self.lock_root, resource):
            if op == "fs_write_new":
                content = str(args.get("content", ""))
                encoding = str(args.get("encoding", "utf-8"))
                final_hash = hashlib.sha256(content.encode(encoding)).hexdigest()
                if path.exists():
                    if path.is_file() and _file_sha256(path) == final_hash:
                        result = {"path": str(path), "sha256": final_hash, "recovered": True}
                        self.ledger.complete(effect_key, result)
                        return {"status": "CACHED", "data": result}
                    raise MissionError("target already exists")
                path.parent.mkdir(parents=True, exist_ok=True)
                tmp = path.with_name(path.name + f".sentinela-{os.getpid()}.tmp")
                tmp.write_text(content, encoding=encoding)
                os.replace(tmp, path)
                result = {"path": str(path), "sha256": _file_sha256(path), "created": True}
                self.ledger.complete(effect_key, result)
                return {"status": "SUCCESS", "data": result}
            if op == "fs_patch_cas":
                if not path.is_file():
                    raise MissionError("patch target not found")
                expected = str(args.get("expected_sha256", "")).lower()
                old = str(args.get("old_text", ""))
                new = str(args.get("new_text", ""))
                encoding = str(args.get("encoding", "utf-8"))
                current_bytes = path.read_bytes()
                current_hash = hashlib.sha256(current_bytes).hexdigest()
                text = current_bytes.decode(encoding)
                if text.count(old) == 1:
                    desired_text = text.replace(old, new, 1)
                    desired_bytes = desired_text.encode(encoding)
                    desired_hash = hashlib.sha256(desired_bytes).hexdigest()
                else:
                    desired_hash = None
                if current_hash != expected:
                    if begin["existing"] and desired_hash and current_hash == desired_hash:
                        result = {"path": str(path), "sha256": current_hash, "recovered": True}
                        self.ledger.complete(effect_key, result)
                        return {"status": "CACHED", "data": result}
                    raise MissionError("CAS precondition failed")
                if text.count(old) != 1:
                    raise MissionError("old_text must occur exactly once")
                tmp = path.with_name(path.name + f".sentinela-{os.getpid()}.tmp")
                tmp.write_bytes(desired_bytes)
                os.replace(tmp, path)
                result = {"path": str(path), "before_sha256": expected, "sha256": _file_sha256(path), "patched": True}
                self.ledger.complete(effect_key, result)
                return {"status": "SUCCESS", "data": result}
        raise MissionError("unknown write operation")


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise MissionError("mission root must be an object")
    return data


def _command_paths_for_commit(workspace: Path, sha: str) -> list[Path]:
    p = subprocess.run(
        ["git", "-C", str(workspace), "diff-tree", "--root", "--no-commit-id", "--name-only", "-r", sha, "--", "transport/commands"],
        capture_output=True, text=True, timeout=20, check=True,
    )
    out = []
    for rel in p.stdout.splitlines():
        rel = rel.strip().replace("\\", "/")
        if rel.startswith("transport/commands/") and rel.endswith(".json"):
            candidate = (workspace / rel).resolve()
            if os.path.commonpath([str(candidate), str(workspace.resolve())]) == str(workspace.resolve()) and candidate.is_file():
                out.append(candidate)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mission")
    ap.add_argument("--workspace")
    ap.add_argument("--git-sha")
    ns = ap.parse_args()
    dispatcher = Dispatcher()
    paths: list[Path]
    if ns.mission:
        paths = [Path(ns.mission).resolve()]
    elif ns.workspace and ns.git_sha:
        paths = _command_paths_for_commit(Path(ns.workspace), ns.git_sha)
    else:
        raise SystemExit("provide --mission or --workspace with --git-sha")
    if not paths:
        print(RESULT_MARKER + json.dumps({"schema": "sentinela-mission-receipt/1", "status": "NO_COMMANDS", "instruction_authority": "NONE"}, separators=(",", ":")))
        return 0
    exit_code = 0
    for path in paths:
        try:
            receipt = dispatcher.run(_load_json(path))
        except Exception as exc:
            receipt = {"schema": "sentinela-mission-receipt/1", "status": "ERROR", "error": f"{type(exc).__name__}: {exc}", "source": str(path), "instruction_authority": "NONE"}
            exit_code = 2
        print(RESULT_MARKER + json.dumps(receipt, ensure_ascii=False, separators=(",", ":")))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
