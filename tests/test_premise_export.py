import tempfile, unittest
from pathlib import Path
import sentinela
from premise_export import compile_bundle, PROFILES

class PremiseExportTests(unittest.TestCase):
    def packet(self):
        d=tempfile.TemporaryDirectory(); p=Path(d.name)/"p.json"
        sentinela.save(p,{"format":sentinela.FORMAT,"entries":[]})
        old=sentinela.append(p,"decision","human","Plano A")
        sentinela.append(p,"correction","human","Plano B",revises=old["id"])
        sentinela.append(p,"boundary","human","Sem gasto sem autorizacao")
        return d,sentinela.load(p)

    def test_all_profiles_compile_same_verified_state(self):
        d,packet=self.packet()
        try:
            bundles=[compile_bundle(packet,p) for p in sorted(PROFILES)]
            for b in bundles:
                self.assertIn("Plano B",b["runtime_text"])
                self.assertNotIn("Plano A. Fonte",b["runtime_text"])
                self.assertIn("Sem gasto sem autorizacao",b["runtime_text"])
                self.assertEqual("decision",b["human_audit"]["vale_agora"][0]["papel"])
        finally: d.cleanup()

    def test_bundle_keeps_source_ids(self):
        d,packet=self.packet()
        try:
            b=compile_bundle(packet,"fresh-chat")
            self.assertIn("Fonte: E0002",b["runtime_text"])
            self.assertIn("Fonte: E0003",b["runtime_text"])
        finally: d.cleanup()

    def test_invalid_packet_refuses_export(self):
        d,packet=self.packet()
        try:
            packet["entries"][0]["text"]="tampered"
            with self.assertRaises(ValueError): compile_bundle(packet,"fresh-chat")
        finally: d.cleanup()

    def test_unknown_profile_refused(self):
        d,packet=self.packet()
        try:
            with self.assertRaises(ValueError): compile_bundle(packet,"magic")
        finally: d.cleanup()

if __name__=="__main__": unittest.main()
