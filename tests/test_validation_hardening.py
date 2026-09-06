import unittest
import sentinela

class ValidationHardeningTests(unittest.TestCase):
    def entry(self, **changes):
        e={"id":"E0001","time":"x","actor":"human","kind":"observation","text":"x","status":"active","confidence":None,"evidence":[],"revises":None,"prev_hash":"GENESIS"}
        e.update(changes); e["hash"]=sentinela.digest(e); return e
    def packet(self,e): return {"format":sentinela.FORMAT,"entries":[e]}
    def test_confidence_out_of_range(self): self.assertTrue(any("invalid confidence" in x for x in sentinela.verify(self.packet(self.entry(confidence=2)))))
    def test_evidence_must_be_strings(self): self.assertTrue(any("invalid evidence" in x for x in sentinela.verify(self.packet(self.entry(evidence=[123])))))
    def test_empty_actor_rejected(self): self.assertTrue(any("invalid actor" in x for x in sentinela.verify(self.packet(self.entry(actor="")))))
    def test_missing_required_field(self):
        e=self.entry(); del e["text"]; e["hash"]=sentinela.digest(e)
        self.assertTrue(any("missing fields text" in x for x in sentinela.verify(self.packet(e))))
    def test_non_list_entries_fails_closed(self): self.assertIn("entries must be list", sentinela.verify({"format":sentinela.FORMAT,"entries":{}}))
    def test_inactive_revision_does_not_replace_active_state(self):
        a=self.entry(); b={"id":"E0002","time":"x","actor":"human","kind":"correction","text":"no","status":"rejected","confidence":None,"evidence":[],"revises":"E0001","prev_hash":a["hash"]}; b["hash"]=sentinela.digest(b)
        p={"format":sentinela.FORMAT,"entries":[a,b]}; self.assertEqual(["E0001"],[e["id"] for e in sentinela.current(p)])
    def test_self_revision_rejected(self):
        e=self.entry(revises="E0001"); self.assertTrue(any("revises unknown/future id" in x for x in sentinela.verify(self.packet(e))))
    def test_extra_entry_field_rejected(self):
        e=self.entry(extra="hidden-state"); self.assertTrue(any("unsupported fields extra" in x for x in sentinela.verify(self.packet(e))))
    def test_extra_packet_field_rejected(self):
        p=self.packet(self.entry()); p["hidden"]={}; self.assertIn("packet has unsupported fields",sentinela.verify(p))

if __name__=="__main__": unittest.main()
