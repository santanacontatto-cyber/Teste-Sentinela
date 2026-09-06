import tempfile, unittest
from pathlib import Path
import sentinela

class PremiseLayerTests(unittest.TestCase):
    def build(self):
        d=tempfile.TemporaryDirectory(); p=Path(d.name)/"p.json"
        sentinela.save(p,{"format":sentinela.FORMAT,"entries":[]})
        old=sentinela.append(p,"decision","human","Usar estrategia A")
        new=sentinela.append(p,"correction","human","Usar estrategia B",revises=old["id"])
        boundary=sentinela.append(p,"boundary","human","Nao gastar sem autorizacao")
        uncertain=sentinela.append(p,"interpretation","ai","B talvez seja melhor",confidence=.2)
        return d,p,sentinela.load(p),old,new,boundary,uncertain

    def test_correction_inherits_decision_role(self):
        d,p,packet,old,new,_,_=self.build()
        try: self.assertEqual("decision",sentinela.effective_kind(new,packet))
        finally: d.cleanup()

    def test_human_view_exposes_before_and_now(self):
        d,p,packet,old,new,_,_=self.build()
        try:
            view=sentinela.human_view(packet)
            self.assertEqual(["E0002","E0003","E0004"],[x["id"] for x in view["vale_agora"]])
            self.assertEqual("decision",view["vale_agora"][0]["papel"])
            self.assertEqual("E0002",view["valia_antes"][0]["substituido_por"])
        finally: d.cleanup()

    def test_premise_block_preserves_uncertainty_and_sources(self):
        d,p,packet,_,_,_,_=self.build()
        try:
            text=sentinela.premise_block(packet)
            self.assertIn("DECISAO ATUAL",text)
            self.assertIn("Fonte: E0002",text)
            self.assertIn("Substitui: E0001",text)
            self.assertIn("Confianca registrada: 0.20",text)
            self.assertNotIn("Usar estrategia A. Fonte",text)
        finally: d.cleanup()

    def test_correction_inherits_uncertainty_when_not_redeclared(self):
        d=tempfile.TemporaryDirectory(); p=Path(d.name)/"p.json"
        try:
            sentinela.save(p,{"format":sentinela.FORMAT,"entries":[]})
            old=sentinela.append(p,"interpretation","ai","Hipotese antiga",confidence=.25)
            new=sentinela.append(p,"correction","ai","Hipotese corrigida",revises=old["id"])
            packet=sentinela.load(p)
            self.assertEqual("interpretation",sentinela.effective_kind(new,packet))
            self.assertEqual(.25,sentinela.effective_confidence(new,packet))
            view=sentinela.human_view(packet)
            self.assertTrue(view["vale_agora"][0]["incerto"])
            self.assertIn("Confianca registrada: 0.25",sentinela.premise_block(packet))
        finally: d.cleanup()

    def test_new_confidence_overrides_inherited_confidence(self):
        d=tempfile.TemporaryDirectory(); p=Path(d.name)/"p.json"
        try:
            sentinela.save(p,{"format":sentinela.FORMAT,"entries":[]})
            old=sentinela.append(p,"interpretation","ai","Hipotese antiga",confidence=.25)
            new=sentinela.append(p,"correction","ai","Hipotese confirmada",revises=old["id"],confidence=.9)
            packet=sentinela.load(p)
            self.assertEqual(.9,sentinela.effective_confidence(new,packet))
            self.assertFalse(sentinela.human_view(packet)["vale_agora"][0]["incerto"])
        finally: d.cleanup()

    def test_projections_fail_closed_on_tamper(self):
        d,p,packet,_,_,_,_=self.build()
        try:
            packet["entries"][0]["text"]="adulterado"
            with self.assertRaises(ValueError): sentinela.human_view(packet)
            with self.assertRaises(ValueError): sentinela.premise_block(packet)
        finally: d.cleanup()

if __name__=="__main__": unittest.main()
