#!/usr/bin/env python3
"""Sentinela Continuity Packet v0 — local, deterministic, stdlib-only."""
from __future__ import annotations
import argparse, hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.1.0"
KINDS = {"observation", "interpretation", "decision", "boundary", "correction"}
STATUS = {"active", "rejected", "superseded"}


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(entry):
    body = {k: v for k, v in entry.items() if k != "hash"}
    return hashlib.sha256(canonical(body).encode()).hexdigest()


def load(path):
    p = Path(path)
    if not p.exists():
        return {"format": "sentinela-continuity-packet/v0", "entries": []}
    return json.loads(p.read_text(encoding="utf-8"))


def save(path, packet):
    Path(path).write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def verify(packet):
    errors, ids = [], set()
    if packet.get("format") != "sentinela-continuity-packet/v0": errors.append("unsupported format")
    prev = "GENESIS"
    for i, e in enumerate(packet.get("entries", [])):
        where = f"entry[{i}]"
        if e.get("id") in ids: errors.append(f"{where}: duplicate id")
        ids.add(e.get("id"))
        if e.get("kind") not in KINDS: errors.append(f"{where}: invalid kind")
        if e.get("status") not in STATUS: errors.append(f"{where}: invalid status")
        if e.get("prev_hash") != prev: errors.append(f"{where}: broken chain")
        if e.get("hash") != digest(e): errors.append(f"{where}: hash mismatch")
        if e.get("revises") and e.get("revises") not in ids: errors.append(f"{where}: revises unknown/future id")
        prev = e.get("hash")
    return errors


def append(path, kind, actor, text, status="active", revises=None, evidence=None, confidence=None):
    packet = load(path)
    errors = verify(packet)
    if errors: raise ValueError("packet invalid; refusing write: " + "; ".join(errors))
    entries = packet["entries"]
    if revises and not any(x["id"] == revises for x in entries): raise ValueError("revises id not found")
    n = len(entries) + 1
    e = {
        "id": f"E{n:04d}", "time": datetime.now(timezone.utc).isoformat(),
        "actor": actor, "kind": kind, "text": text, "status": status,
        "confidence": confidence, "evidence": evidence or [], "revises": revises,
        "prev_hash": entries[-1]["hash"] if entries else "GENESIS"
    }
    e["hash"] = digest(e); entries.append(e); save(path, packet); return e


def current(packet):
    entries = packet.get("entries", []); replaced = {e.get("revises") for e in entries if e.get("revises")}
    return [e for e in entries if e["status"] == "active" and e["id"] not in replaced]


def main():
    ap = argparse.ArgumentParser(prog="sentinela", description="Verifiable human-AI continuity packets")
    ap.add_argument("--version", action="version", version=VERSION)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p=sub.add_parser("init"); p.add_argument("file")
    p=sub.add_parser("add"); p.add_argument("file"); p.add_argument("--kind",required=True,choices=sorted(KINDS)); p.add_argument("--actor",required=True); p.add_argument("--text",required=True); p.add_argument("--status",choices=sorted(STATUS),default="active"); p.add_argument("--revises"); p.add_argument("--evidence",action="append",default=[]); p.add_argument("--confidence",type=float)
    p=sub.add_parser("verify"); p.add_argument("file")
    p=sub.add_parser("current"); p.add_argument("file")
    a=ap.parse_args()
    try:
        if a.cmd=="init":
            if Path(a.file).exists(): raise ValueError("refusing to overwrite existing packet")
            save(a.file,{"format":"sentinela-continuity-packet/v0","entries":[]}); print(a.file)
        elif a.cmd=="add":
            if a.confidence is not None and not 0 <= a.confidence <= 1: raise ValueError("confidence must be 0..1")
            print(json.dumps(append(a.file,a.kind,a.actor,a.text,a.status,a.revises,a.evidence,a.confidence),ensure_ascii=False,indent=2))
        elif a.cmd=="verify":
            errors=verify(load(a.file)); print("PASS" if not errors else "FAIL\n"+"\n".join(errors)); sys.exit(bool(errors))
        elif a.cmd=="current": print(json.dumps(current(load(a.file)),ensure_ascii=False,indent=2))
    except (ValueError, json.JSONDecodeError) as e:
        print(f"ERROR: {e}",file=sys.stderr); sys.exit(2)
if __name__ == "__main__": main()
