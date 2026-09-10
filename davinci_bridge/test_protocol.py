#!/usr/bin/env python3
"""Offline tests for the Sentinela ↔ DaVinci file-mailbox transport.

These tests do not require DaVinci Resolve. They prove that the Python side writes
a request, ignores stale responses, matches request IDs, and receives a response
through the exact mailbox paths used by the Lua bridge.
"""

from __future__ import annotations

import os
import pathlib
import tempfile
import threading
import time
import unittest
from unittest import mock

import send_command


class BridgeProtocolTests(unittest.TestCase):
    def test_parse_response(self) -> None:
        parsed = send_command.parse_response("status=ok\nproject=Sentinela\nempty=\n")
        self.assertEqual(parsed["status"], "ok")
        self.assertEqual(parsed["project"], "Sentinela")
        self.assertEqual(parsed["empty"], "")

    def test_round_trip_ignores_stale_response(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            inbox = root / "inbox"
            outbox = root / "outbox"
            inbox.mkdir(parents=True)
            outbox.mkdir(parents=True)

            # A stale response must never satisfy a fresh command.
            (outbox / "response.txt").write_text(
                "id=old-request\nstatus=ok\nproject=wrong\n",
                encoding="utf-8",
            )

            def fake_lua_listener() -> None:
                request_path = inbox / "request.txt"
                deadline = time.monotonic() + 2.0
                while time.monotonic() < deadline:
                    if request_path.exists():
                        request = send_command.parse_response(
                            request_path.read_text(encoding="utf-8")
                        )
                        request_id = request.get("id")
                        if request_id:
                            send_command.atomic_write(
                                outbox / "response.txt",
                                "\n".join(
                                    [
                                        f"id={request_id}",
                                        "status=ok",
                                        "command=PING",
                                        "product=DaVinci Resolve",
                                        "project=Sentinela_Test",
                                    ]
                                )
                                + "\n",
                            )
                            return
                    time.sleep(0.01)
                raise AssertionError("fake listener did not receive request")

            listener = threading.Thread(target=fake_lua_listener, daemon=True)
            listener.start()

            with mock.patch.dict(os.environ, {"SENTINELA_BRIDGE_HOME": str(root)}):
                result = send_command.send("ping", timeout=2.0)

            listener.join(timeout=1.0)
            self.assertFalse(listener.is_alive())
            self.assertEqual(result["status"], "ok")
            self.assertEqual(result["command"], "PING")
            self.assertEqual(result["project"], "Sentinela_Test")
            self.assertNotEqual(result["id"], "old-request")


if __name__ == "__main__":
    unittest.main()
