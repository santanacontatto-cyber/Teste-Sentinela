import unittest
from continuity_test import score
from sentinela import digest

def packet():
    es=[]
    def add(kind,text,status="active",revises=None,confidence=None):
        e={"id":f"E{len(es)+1:04d}","time":"2026-01-01T00:00:00Z","actor":"human","kind":kind,"text":text,"status":status,"confidence":confidence,"evidence":[],"revises":revises,"prev_hash":es[-1]["hash"] if es else "GENESIS"}; e["hash"]=digest(e); es.append(e); return e
    old=add("decision","old"); add("correction","new",revises=old["id"]); add("boundary","no spending"); add("interpretation","maybe",confidence=.2)
    return {"format":"sentinela-continuity-packet/v0","entries":es}

class ScorerTests(unittest.TestCase):
    def good(self): return {"active_ids":["E0002","E0003","E0004"],"boundaries":["E0003"],"decisions":["E0002"],"uncertain":["E0004"],"citations":["E0002","E0003","E0004"]}
    def test_anonymous_chatgpt_observation_is_now_expected(self): self.assertTrue(score(packet(),self.good())["pass"])
    def test_raw_event_kind_is_not_enough(self):
        a=self.good(); a["decisions"]=[]; self.assertFalse(score(packet(),a)["pass"])
    def test_hallucinated_citation_fails(self):
        a=self.good(); a["citations"]=["E9999"]; self.assertFalse(score(packet(),a)["pass"])
    def test_superseded_state_fails(self):
        a=self.good(); a["active_ids"]=["E0001","E0002","E0003","E0004"]; a["decisions"]=["E0001","E0002"]; self.assertFalse(score(packet(),a)["pass"])
    def test_missing_current_support_fails(self):
        a=self.good(); a["citations"]=["E0002","E0003"]; self.assertFalse(score(packet(),a)["pass"])
    def test_unsupported_answer_field_fails(self):
        a=self.good(); a["persuasive_story"]="unsupported"; self.assertFalse(score(packet(),a)["pass"])
    def test_malformed_packet_fails_closed(self):
        p=packet(); p["entries"][0]["text"]="tampered"; self.assertFalse(score(p,self.good())["pass"])
if __name__=="__main__": unittest.main()
