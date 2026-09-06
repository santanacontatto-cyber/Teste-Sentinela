import unittest
import sentinela

class FailClosedTests(unittest.TestCase):
    def base(self, **overrides):
        e={"id":"E0001","time":"x","actor":"human","kind":"observation","text":"x","status":"active","confidence":None,"evidence":[],"revises":None,"prev_hash":"GENESIS"}; e.update(overrides); e["hash"]=sentinela.digest(e); return {"format":"sentinela-continuity-packet/v0","entries":[e]}
    def test_unknown_format(self):
        p=self.base(); p["format"]="future-format"; self.assertIn("unsupported format",sentinela.verify(p))
    def test_duplicate_id(self):
        p=self.base(); e=dict(p["entries"][0]); e["prev_hash"]=p["entries"][0]["hash"]; e["hash"]=sentinela.digest(e); p["entries"].append(e); self.assertTrue(any("duplicate id" in x for x in sentinela.verify(p)))
    def test_invalid_kind(self): self.assertTrue(any("invalid kind" in x for x in sentinela.verify(self.base(kind="wish"))))
    def test_invalid_status(self): self.assertTrue(any("invalid status" in x for x in sentinela.verify(self.base(status="maybe"))))
if __name__=="__main__": unittest.main()
