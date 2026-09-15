#!/usr/bin/env python3
"""Offline tests for the permanent Sentinela ↔ DaVinci mailbox transport."""

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

    def _with_fake_listener(self, responder, invoke):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            inbox = root / "inbox"
            outbox = root / "outbox"
            inbox.mkdir(parents=True)
            outbox.mkdir(parents=True)
            (outbox / "response.txt").write_text(
                "id=stale\nstatus=ok\nproject=wrong\n", encoding="utf-8"
            )

            seen = {}

            def fake_lua_listener() -> None:
                request_path = inbox / "request.txt"
                deadline = time.monotonic() + 2.0
                while time.monotonic() < deadline:
                    if request_path.exists():
                        request = send_command.parse_response(
                            request_path.read_text(encoding="utf-8")
                        )
                        if request.get("id"):
                            seen.update(request)
                            payload = responder(request)
                            payload["id"] = request["id"]
                            text = "\n".join(f"{k}={v}" for k, v in payload.items()) + "\n"
                            send_command.atomic_write(outbox / "response.txt", text)
                            return
                    time.sleep(0.01)
                raise AssertionError("fake listener did not receive request")

            listener = threading.Thread(target=fake_lua_listener, daemon=True)
            listener.start()
            with mock.patch.dict(os.environ, {"SENTINELA_BRIDGE_HOME": str(root)}):
                result = invoke()
            listener.join(timeout=1.0)
            self.assertFalse(listener.is_alive())
            self.assertNotEqual(result["id"], "stale")
            return seen, result

    def test_ping_round_trip_ignores_stale_response(self) -> None:
        seen, result = self._with_fake_listener(
            lambda req: {"status": "ok", "command": req["command"], "bridge": "SentinelaBridge-v1"},
            lambda: send_command.ping(timeout=2.0),
        )
        self.assertEqual(seen["command"], "PING")
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["bridge"], "SentinelaBridge-v1")

    def test_generic_module_round_trip(self) -> None:
        seen, result = self._with_fake_listener(
            lambda req: {
                "status": "ok",
                "command": req["command"],
                "module": req["module"],
                "echo.page": req.get("arg.page", ""),
            },
            lambda: send_command.run_module(
                "open_page", arguments={"page": "edit"}, timeout=2.0
            ),
        )
        self.assertEqual(seen["command"], "RUN")
        self.assertEqual(seen["module"], "open_page")
        self.assertEqual(seen["arg.page"], "edit")
        self.assertEqual(result["module"], "open_page")
        self.assertEqual(result["echo.page"], "edit")

    def test_rejects_module_path_traversal(self) -> None:
        with self.assertRaises(ValueError):
            send_command.run_module("../evil", timeout=0.01)


if __name__ == "__main__":
    unittest.main()
