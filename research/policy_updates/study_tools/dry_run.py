"""Reproducible checks using synthetic outcomes only; never confirmatory items."""
import json
from pathlib import Path
import platform
import numpy
import scipy
from study_tools import gates, simulation, statistics

config, config_hash = gates.load_config()
output = Path('runs/dry-run-v0')
output.mkdir(parents=True, exist_ok=False)
report = {'config_sha256': config_hash, 'python': platform.python_version(),
          'numpy': numpy.__version__, 'scipy': scipy.__version__, 'scenarios': []}
for baseline in (.03, .10, .20):
    for effect in (0, .05, .08):
        result = simulation.power(config, repetitions=40, seed=20261014,
                                  baseline=baseline, effect=effect)
        report['scenarios'].append(result)
        print(f'Completed baseline={baseline}, effect={effect}', flush=True)
report['label_shuffled'] = simulation.power(config, repetitions=40, seed=20261015,
                                            baseline=.10, effect=.08, shuffle=True)
rows, models = simulation.synthetic(seed=1014)
report['synthetic_analysis'] = statistics.analyze(rows, models, config, bootstrap_reps=1000)
report['pilot_output'] = gates.pilot(rows, models, config)
with (output / 'report.json').open('x') as stream:
    json.dump(report, stream, indent=2, allow_nan=False)
print('Saved synthetic dry-run report.', flush=True)
