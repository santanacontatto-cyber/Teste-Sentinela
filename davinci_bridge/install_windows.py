#!/usr/bin/env python3
"""Install SentinelaBridge for the current Windows user.

No admin rights, PowerShell, registry edits, services, sockets, or third-party
packages. It copies the Lua script into Resolve's per-user Utility scripts
folder and creates the local mailbox directories.
"""

from __future__ import annotations

import os
import pathlib
import shutil
import sys


def main() -> int:
    if os.name != "nt":
        print("This installer is for Windows only.", file=sys.stderr)
        return 2

    here = pathlib.Path(__file__).resolve().parent
    source = here / "SentinelaBridge.lua"
    if not source.exists():
        print(f"Missing source script: {source}", file=sys.stderr)
        return 2

    appdata = os.environ.get("APPDATA")
    if not appdata:
        print("APPDATA is not available.", file=sys.stderr)
        return 2

    target_dir = (
        pathlib.Path(appdata)
        / "Blackmagic Design"
        / "DaVinci Resolve"
        / "Support"
        / "Fusion"
        / "Scripts"
        / "Utility"
    )
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "SentinelaBridge.lua"
    shutil.copy2(source, target)

    root = pathlib.Path(os.environ.get("SENTINELA_BRIDGE_HOME", pathlib.Path.home() / "SentinelaBridge"))
    for name in ("inbox", "outbox", "logs"):
        (root / name).mkdir(parents=True, exist_ok=True)

    print("SentinelaBridge installed.")
    print(f"Lua script: {target}")
    print(f"Mailbox:    {root}")
    print("Next: restart Resolve if it was open, then run Workspace > Scripts > SentinelaBridge once.")
    print("Test: python send_command.py ping")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
