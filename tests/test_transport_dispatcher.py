import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from transport.dispatcher import Dispatcher, MissionError


class DispatcherTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.allowed = base / "allowed"
        self.state = base / "state"
        self.allowed.mkdir()
        self.d = Dispatcher([self.allowed], self.state, max_workers=4)

    def tearDown(self):
        self.tmp.cleanup()

    def mission(self, steps, mode="read_only", mission_id="mission-test-0001"):
        return {
            "version": 1,
            "mission_id": mission_id,
            "workframe_id": "wf-test",
            "mode": mode,
            "instruction_authority": "NONE",
            "steps": steps,
        }

    def test_health(self):
        r = self.d.run(self.mission([{"id": "h", "op": "health"}]))
        self.assertEqual(r["status"], "SUCCESS")
        self.assertTrue(r["steps"]["h"]["data"]["ok"])

    def test_read_and_search_are_bounded_to_allowed_root(self):
        p = self.allowed / "a.txt"
        p.write_text("alpha\nneedle here\nomega\n", encoding="utf-8")
        r = self.d.run(self.mission([
            {"id": "r", "op": "fs_read", "args": {"path": str(p)}},
            {"id": "s", "op": "fs_search", "args": {"root": str(self.allowed), "query": "needle"}, "depends_on": ["r"]},
        ]))
        self.assertEqual(r["status"], "SUCCESS")
        self.assertEqual(len(r["steps"]["s"]["data"]["matches"]), 1)

    def test_path_escape_is_rejected(self):
        outside = Path(self.tmp.name) / "outside.txt"
        outside.write_text("x", encoding="utf-8")
        r = self.d.run(self.mission([{"id": "r", "op": "fs_read", "args": {"path": str(outside)}}]))
        self.assertEqual(r["status"], "ERROR")
        self.assertIn("outside allowed roots", r["steps"]["r"]["error"])

    def test_write_requires_controlled_write(self):
        target = self.allowed / "new.txt"
        with self.assertRaises(MissionError):
            self.d.run(self.mission([
                {"id": "w", "op": "fs_write_new", "effect_key": "fx-00000001", "args": {"path": str(target), "content": "x"}}
            ]))

    def test_write_new_is_idempotent(self):
        target = self.allowed / "new.txt"
        m = self.mission([
            {"id": "w", "op": "fs_write_new", "effect_key": "fx-create-0001", "args": {"path": str(target), "content": "hello"}}
        ], mode="controlled_write")
        a = self.d.run(m)
        b = self.d.run(m)
        self.assertEqual(a["steps"]["w"]["status"], "SUCCESS")
        self.assertEqual(b["steps"]["w"]["status"], "CACHED")
        self.assertEqual(target.read_text(encoding="utf-8"), "hello")

    def test_effect_key_cannot_change_intent(self):
        a = self.allowed / "a.txt"
        b = self.allowed / "b.txt"
        one = self.mission([
            {"id": "w", "op": "fs_write_new", "effect_key": "fx-same-00001", "args": {"path": str(a), "content": "a"}}
        ], mode="controlled_write", mission_id="mission-test-0002")
        two = self.mission([
            {"id": "w", "op": "fs_write_new", "effect_key": "fx-same-00001", "args": {"path": str(b), "content": "b"}}
        ], mode="controlled_write", mission_id="mission-test-0003")
        self.assertEqual(self.d.run(one)["status"], "SUCCESS")
        r = self.d.run(two)
        self.assertEqual(r["status"], "ERROR")
        self.assertIn("different intent", r["steps"]["w"]["error"])

    def test_patch_cas_accepts_expected_hash_and_rejects_stale(self):
        p = self.allowed / "p.txt"
        p.write_text("before", encoding="utf-8")
        expected = hashlib.sha256(b"before").hexdigest()
        good = self.mission([
            {"id": "p", "op": "fs_patch_cas", "effect_key": "fx-patch-0001",
             "args": {"path": str(p), "expected_sha256": expected, "old_text": "before", "new_text": "after"}}
        ], mode="controlled_write", mission_id="mission-test-0004")
        self.assertEqual(self.d.run(good)["status"], "SUCCESS")
        self.assertEqual(p.read_text(encoding="utf-8"), "after")
        stale = self.mission([
            {"id": "p", "op": "fs_patch_cas", "effect_key": "fx-patch-0002",
             "args": {"path": str(p), "expected_sha256": expected, "old_text": "before", "new_text": "other"}}
        ], mode="controlled_write", mission_id="mission-test-0005")
        r = self.d.run(stale)
        self.assertEqual(r["status"], "ERROR")
        self.assertIn("CAS precondition failed", r["steps"]["p"]["error"])

    def test_failed_dependency_does_not_run_dependent(self):
        outside = Path(self.tmp.name) / "outside.txt"
        outside.write_text("x", encoding="utf-8")
        r = self.d.run(self.mission([
            {"id": "bad", "op": "fs_read", "args": {"path": str(outside)}},
            {"id": "later", "op": "health", "depends_on": ["bad"]},
        ]))
        self.assertEqual(r["steps"]["bad"]["status"], "ERROR")
        self.assertEqual(r["steps"]["later"]["status"], "SKIPPED_DEPENDENCY")

    def test_cycle_is_rejected_at_runtime(self):
        with self.assertRaises(MissionError):
            self.d.run(self.mission([
                {"id": "a", "op": "health", "depends_on": ["b"]},
                {"id": "b", "op": "health", "depends_on": ["a"]},
            ]))


if __name__ == "__main__":
    unittest.main()
