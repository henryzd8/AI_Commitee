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
            subprocess.run([sys.executable,'-m','item_generator','export-harness',str(root/'probes.jsonl'),str(root/'histories.jsonl'),str(root/'export')],check=True,capture_output=True)
            sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'harness'/'src'))
            from pu.schemas import Item, from_dict
            exported=[from_dict(Item,json.loads(line)) for line in (root/'export'/'items.jsonl').read_text().splitlines()]
            history_exported=[from_dict(Item,json.loads(line)) for line in (root/'export'/'history_items.jsonl').read_text().splitlines()]
            self.assertEqual(len(exported),100)
            self.assertTrue(all(len(p.history_item_ids)==4 for p in exported))
            self.assertEqual({h.item_id for h in history_exported},{h for p in exported for h in p.history_item_ids})
