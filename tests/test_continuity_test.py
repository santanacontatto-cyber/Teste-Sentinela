import unittest
from continuity_test import score
from sentinela import digest

def packet():
    es=[]
    def add(kind,text,status="active",revises=None,confidence=None):
        e={"id":f"E{len(es)+1:04d}","time":"2026-01-01T00:00:00Z","actor":"human","kind":kind,"text":text,"status":status,"confidence":confidence,"evidence":[],"revises":revises,"prev_hash":es[-1]["hash"] if es else "GENESIS"}; e["hash"]=digest(e); es.append(e); return e
    old=add("decision","old")
    add("correction","new",revises=old["id"])
    add("boundary","no spending")
    add("interpretation","maybe",confidence=.2)
    return {"format":"sentinela-continuity-packet/v0","entries":es}

class ScorerTests(unittest.TestCase):
    def test_perfect_reconstruction(self):
        a={"active_ids":["E0002","E0003","E0004"],"boundaries":["E0003"],"decisions":[],"uncertain":["E0004"],"citations":["E0002","E0003"]}
        self.assertTrue(score(packet(),a)["pass"])
    def test_hallucinated_citation_fails(self):
        a={"active_ids":["E0002","E0003","E0004"],"boundaries":["E0003"],"decisions":[],"uncertain":["E0004"],"citations":["E9999"]}
        self.assertFalse(score(packet(),a)["pass"])
    def test_superseded_state_fails(self):
        a={"active_ids":["E0001","E0002","E0003","E0004"],"boundaries":["E0003"],"decisions":["E0001"],"uncertain":["E0004"],"citations":[]}
        self.assertFalse(score(packet(),a)["pass"])
if __name__=="__main__": unittest.main()
