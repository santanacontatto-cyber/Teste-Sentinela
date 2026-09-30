#!/usr/bin/env python3
"""Instala a ponte Sentinela ↔ DaVinci para o usuário atual do Windows.

Sem admin, PowerShell, registro, serviços, sockets ou pacotes de terceiros.
Copia o listener Lua para o menu Scripts do Resolve e sincroniza módulos Lua
para a pasta local da ponte.
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
    bridge_source = here / "SentinelaBridge.lua"
    modules_source = here / "modules"
    if not bridge_source.exists():
        print(f"Missing bridge script: {bridge_source}", file=sys.stderr)
        return 2
    if not modules_source.is_dir():
        print(f"Missing modules directory: {modules_source}", file=sys.stderr)
        return 2

    appdata = os.environ.get("APPDATA")
    if not appdata:
        print("APPDATA is not available.", file=sys.stderr)
        return 2

    resolve_scripts = (
        pathlib.Path(appdata)
        / "Blackmagic Design"
        / "DaVinci Resolve"
        / "Support"
        / "Fusion"
        / "Scripts"
        / "Utility"
    )
    resolve_scripts.mkdir(parents=True, exist_ok=True)
    bridge_target = resolve_scripts / "SentinelaBridge.lua"
    shutil.copy2(bridge_source, bridge_target)

    root = pathlib.Path(
        os.environ.get("SENTINELA_BRIDGE_HOME", str(pathlib.Path.home() / "SentinelaBridge"))
    )
    for name in ("inbox", "outbox", "logs", "modules"):
        (root / name).mkdir(parents=True, exist_ok=True)

    copied_modules: list[str] = []
    for source in sorted(modules_source.glob("*.lua")):
        target = root / "modules" / source.name
        shutil.copy2(source, target)
        copied_modules.append(source.name)

    print("SentinelaBridge installed/synced.")
    print(f"Bridge Lua: {bridge_target}")
    print(f"Mailbox:    {root}")
    print(f"Modules:    {root / 'modules'}")
    for name in copied_modules:
        print(f"  + {name}")
    print("Next: restart Resolve if needed, then run Workspace > Scripts > SentinelaBridge once.")
    print("Test: python davinci_bridge/send_command.py ping")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
