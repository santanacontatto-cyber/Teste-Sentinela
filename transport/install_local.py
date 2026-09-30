from __future__ import annotations
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

SOURCE = Path(__file__).with_name("dispatcher.py")
ROOT = Path(os.environ.get("LOCALAPPDATA", ".")) / "Sentinela_Transport"
TARGET = ROOT / "dispatcher.py"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if not SOURCE.is_file():
        raise SystemExit("dispatcher.py not found beside installer")
    ROOT.mkdir(parents=True, exist_ok=True)
    before = sha256(SOURCE)
    tmp = TARGET.with_suffix(".py.tmp")
    shutil.copy2(SOURCE, tmp)
    if sha256(tmp) != before:
        tmp.unlink(missing_ok=True)
        raise SystemExit("copy verification failed")
    os.replace(tmp, TARGET)
    receipt = {
        "schema": "sentinela-transport-install/1",
        "installed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "python": sys.executable,
        "source": str(SOURCE),
        "target": str(TARGET),
        "sha256": before,
        "instruction_authority": "NONE",
    }
    (ROOT / "install_receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
