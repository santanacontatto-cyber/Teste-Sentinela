import json, tempfile, unittest
from pathlib import Path
import sentinela

class ContinuityTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.p=Path(self.tmp.name)/"packet.json"
        sentinela.save(self.p,{"format":"sentinela-continuity-packet/v0","entries":[]})
    def tearDown(self): self.tmp.cleanup()
    def test_chain_and_current_revision(self):
        a=sentinela.append(self.p,"decision","human","Use A")
        b=sentinela.append(self.p,"correction","human","Use B",revises=a["id"])
        packet=sentinela.load(self.p)
        self.assertEqual([],sentinela.verify(packet))
        self.assertEqual([b["id"]],[x["id"] for x in sentinela.current(packet)])
    def test_tamper_detected(self):
        sentinela.append(self.p,"boundary","human","Never spend money")
        packet=sentinela.load(self.p); packet["entries"][0]["text"]="Spend money"
        self.assertTrue(sentinela.verify(packet))
    def test_broken_chain_detected(self):
        sentinela.append(self.p,"observation","human","one")
        sentinela.append(self.p,"observation","ai","two")
        packet=sentinela.load(self.p); packet["entries"][1]["prev_hash"]="bad"; packet["entries"][1]["hash"]=sentinela.digest(packet["entries"][1])
        self.assertIn("entry[1]: broken chain",sentinela.verify(packet))
    def test_future_revision_rejected(self):
        packet=sentinela.load(self.p)
        e={"id":"E0001","time":"x","actor":"x","kind":"correction","text":"x","status":"active","confidence":None,"evidence":[],"revises":"E9999","prev_hash":"GENESIS"}; e["hash"]=sentinela.digest(e); packet["entries"].append(e)
        self.assertIn("entry[0]: revises unknown/future id",sentinela.verify(packet))

if __name__ == "__main__": unittest.main()
