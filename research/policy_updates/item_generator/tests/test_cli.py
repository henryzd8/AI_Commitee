import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

class CliTests(unittest.TestCase):
    def test_generation_histories_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            command=[sys.executable,'-m','item_generator','generate','exploration',str(root/'probes.jsonl'),'--seed','A']
            subprocess.run(command,check=True,capture_output=True)
            self.assertNotEqual(subprocess.run(command,capture_output=True).returncode,0)
            subprocess.run([sys.executable,'-m','item_generator','histories',str(root/'probes.jsonl'),str(root/'histories.jsonl')],check=True,capture_output=True)
            probes=[json.loads(line) for line in (root/'probes.jsonl').read_text().splitlines()]
            histories=[json.loads(line) for line in (root/'histories.jsonl').read_text().splitlines()]
            self.assertEqual(len(probes),100)
            self.assertEqual(len(histories),400)
            self.assertEqual({h['probe_item_id'] for h in histories},{p['item_id'] for p in probes})
