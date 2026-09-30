#!/usr/bin/env python3
"""Cliente local da ponte Sentinela ↔ DaVinci.

Biblioteca padrão apenas. O processo externo escreve uma requisição na mailbox;
o Lua dentro do Resolve lê, executa um módulo Lua local e devolve a resposta.
"""

from __future__ import annotations

import argparse
import os
import pathlib
import re
import tempfile
import time
import uuid

_SAFE_NAME = re.compile(r"^[A-Za-z0-9_-]+$")
_SAFE_KEY = re.compile(r"^[A-Za-z0-9_.-]+$")


def bridge_home() -> pathlib.Path:
    configured = os.environ.get("SENTINELA_BRIDGE_HOME")
    if configured:
        return pathlib.Path(configured).expanduser()
    return pathlib.Path.home() / "SentinelaBridge"


def atomic_write(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def parse_response(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw in text.splitlines():
        if "=" in raw:
            key, value = raw.split("=", 1)
            result[key.strip()] = value.strip()
    return result


def _clean_value(value: str) -> str:
    if "\n" in value or "\r" in value:
        raise ValueError("argument values cannot contain newlines")
    return value


def _parse_arg(item: str) -> tuple[str, str]:
    if "=" not in item:
        raise argparse.ArgumentTypeError("--arg must be KEY=VALUE")
    key, value = item.split("=", 1)
    if not _SAFE_KEY.fullmatch(key):
        raise argparse.ArgumentTypeError(f"invalid argument key: {key!r}")
    try:
        value = _clean_value(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc
    return key, value


def _round_trip(fields: list[str], *, timeout: float) -> dict[str, str]:
    root = bridge_home()
    request = root / "inbox" / "request.txt"
    response = root / "outbox" / "response.txt"
    request_id = f"{int(time.time() * 1000)}-{uuid.uuid4().hex[:8]}"
    atomic_write(request, "\n".join([f"id={request_id}", *fields]) + "\n")

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            data = parse_response(response.read_text(encoding="utf-8"))
        except FileNotFoundError:
            data = {}
        if data.get("id") == request_id:
            return data
        time.sleep(0.2)

    raise TimeoutError(
        f"No response in {timeout:g}s. Start Workspace > Scripts > SentinelaBridge in Resolve. "
        f"Mailbox: {root}"
    )


def ping(*, timeout: float = 20.0) -> dict[str, str]:
    return _round_trip(["command=PING"], timeout=timeout)


def stop_bridge(*, timeout: float = 20.0) -> dict[str, str]:
    return _round_trip(["command=STOP_BRIDGE"], timeout=timeout)


def run_module(
    module: str,
    *,
    arguments: dict[str, str] | None = None,
    timeout: float = 20.0,
) -> dict[str, str]:
    if not _SAFE_NAME.fullmatch(module):
        raise ValueError(f"invalid module name: {module!r}")

    fields = ["command=RUN", f"module={module}"]
    for key, value in sorted((arguments or {}).items()):
        if not _SAFE_KEY.fullmatch(key):
            raise ValueError(f"invalid argument key: {key!r}")
        fields.append(f"arg.{key}={_clean_value(value)}")
    return _round_trip(fields, timeout=timeout)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sentinela ↔ DaVinci bridge client")
    parser.add_argument("--timeout", type=float, default=20.0)
    sub = parser.add_subparsers(dest="action", required=True)

    sub.add_parser("ping", help="test the permanent bridge")
    sub.add_parser("stop", help="stop the bridge listener")

    run = sub.add_parser("run", help="run a Lua module already deployed to the bridge")
    run.add_argument("module")
    run.add_argument("--arg", action="append", default=[], type=_parse_arg, metavar="KEY=VALUE")

    args = parser.parse_args()
    if args.action == "ping":
        result = ping(timeout=args.timeout)
    elif args.action == "stop":
        result = stop_bridge(timeout=args.timeout)
    else:
        values = dict(args.arg)
        result = run_module(args.module, arguments=values, timeout=args.timeout)

    for key in sorted(result):
        print(f"{key}={result[key]}")
    return 0 if result.get("status") == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
