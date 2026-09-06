import subprocess, sys, unittest

class EndToEndTests(unittest.TestCase):
    def test_reconstruction_demo(self):
        p=subprocess.run([sys.executable,"examples/run_reconstruction_demo.py"],capture_output=True,text=True)
        self.assertEqual(0,p.returncode,p.stdout+p.stderr)
        self.assertIn('"valid_reconstruction"',p.stdout)
        self.assertIn('"stale_reconstruction"',p.stdout)
        self.assertIn('"hallucinated_evidence"',p.stdout)

if __name__=="__main__": unittest.main()
