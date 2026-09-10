#!/usr/bin/env python3
"""Send commands to SentinelaBridge through a local file mailbox.

Standard-library only. This process does not connect to the Resolve API; the Lua
script running inside Resolve reads request.txt and writes response.txt.
"""

from __future__ import annotations

import argparse
import os
import pathlib
import tempfile
import time
import uuid


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


def send(command: str, *, page: str | None = None, timeout: float = 20.0) -> dict[str, str]:
    root = bridge_home()
    request = root / "inbox" / "request.txt"
    response = root / "outbox" / "response.txt"
    request_id = f"{int(time.time() * 1000)}-{uuid.uuid4().hex[:8]}"

    fields = [f"id={request_id}", f"command={command.upper()}"]
    if page:
        fields.append(f"page={page.lower()}")
    atomic_write(request, "\n".join(fields) + "\n")

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


def main() -> int:
    parser = argparse.ArgumentParser(description="Send a command to SentinelaBridge")
    parser.add_argument(
        "command",
        choices=["ping", "project_info", "open_page", "save_project", "stop_bridge"],
    )
    parser.add_argument("--page", choices=["media", "cut", "edit", "fusion", "color", "fairlight", "deliver"])
    parser.add_argument("--timeout", type=float, default=20.0)
    args = parser.parse_args()

    if args.command == "open_page" and not args.page:
        parser.error("open_page requires --page")

    result = send(args.command, page=args.page, timeout=args.timeout)
    for key in sorted(result):
        print(f"{key}={result[key]}")
    return 0 if result.get("status") == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
