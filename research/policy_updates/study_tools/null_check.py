"""Independent-seed null calibration; outputs synthetic data summaries only."""
import json
from pathlib import Path
from study_tools import gates, simulation

config, config_hash = gates.load_config()
result = simulation.power(config, repetitions=200, seed=991000,
                          baseline=.03, effect=0)
target = Path('runs/null-check-v0.json')
target.parent.mkdir(exist_ok=True)
with target.open('x') as stream:
    json.dump({'config_sha256': config_hash, 'result': result}, stream, indent=2)
print(json.dumps(result, indent=2))
