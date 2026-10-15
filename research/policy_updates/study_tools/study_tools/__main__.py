import argparse
import json
from pathlib import Path
from . import gates, statistics, blinding, simulation

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def rows(path):
    return [json.loads(line) for line in Path(path).read_text(encoding='utf-8-sig').splitlines() if line.strip()]

def write(path, value, jsonl=False):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('x', encoding='utf-8') as stream:
        if jsonl:
            for r in value:
                stream.write(json.dumps(r, allow_nan=False) + '\n')
        else:
            json.dump(value, stream, indent=2, allow_nan=False)

def main():
    parser = argparse.ArgumentParser(description='Policy-update development tooling')
    parser.add_argument('--config', help='reviewed gate configuration; output records its hash')
    commands = parser.add_subparsers(dest='command', required=True)
    freeze = commands.add_parser('freeze-config')
    freeze.add_argument('output')
    freeze.add_argument('--reviewer', required=True)
    b = commands.add_parser('blind')
    b.add_argument('input')
    b.add_argument('directory')
    a = commands.add_parser('analyze')
    a.add_argument('input')
    a.add_argument('output')
    a.add_argument('--models', nargs='+', required=True)
    a.add_argument('--bootstrap', type=int, default=2000)
    a.add_argument('--items', required=True, help='frozen final item JSONL, after collision replacements')
    for name in ('screen', 'manipulation', 'pilot'):
        p = commands.add_parser(name)
        p.add_argument('input')
        p.add_argument('--models', nargs='+', required=True)
        if name != 'pilot':
            p.add_argument('output')
    l = commands.add_parser('label-gate')
    l.add_argument('input')
    s = commands.add_parser('simulate')
    s.add_argument('output')
    s.add_argument('--repetitions', type=int, default=100)
    s.add_argument('--items-per-family', type=int, default=15)
    s.add_argument('--seed', type=int, default=2026)
    args = parser.parse_args()
    config, config_hash = gates.load_config(args.config)
    if args.command == 'freeze-config':
        from datetime import datetime, timezone
        write(args.output, {**config, 'frozen': True, 'reviewer': args.reviewer, 'frozen_at': datetime.now(timezone.utc).isoformat(), 'parent_sha256': config_hash})
    elif args.command == 'blind':
        folder = Path(args.directory)
        if folder.exists():
            raise ValueError('output directory must be new')
        public, private = blinding.blind(rows(args.input))
        write(folder / 'public.jsonl', public, True)
        write(folder / 'private' / 'key.json', private)
    elif args.command == 'pilot':
        print(gates.pilot(rows(args.input), args.models, config))
    elif args.command == 'label-gate':
        print('PASS' if gates.label_gate(read(args.input), config) else 'FAIL')
    else:
        if args.command == 'analyze':
            result = statistics.analyze(rows(args.input), args.models, config, bootstrap_reps=args.bootstrap, expected_items=rows(args.items))
        elif args.command == 'screen':
            result = gates.family_screen(rows(args.input), args.models, config)
        elif args.command == 'manipulation':
            result = gates.manipulation(rows(args.input), args.models, config)
        else:
            result = {'scenarios': []}
            for baseline in (0.03, 0.1, 0.2):
                for effect in (0, 0.05, 0.08):
                    result['scenarios'].append(simulation.power(config, args.repetitions, args.seed, baseline=baseline, effect=effect, items_per_family=args.items_per_family))
        write(args.output, {'config_sha256': config_hash, 'config_version': config['version'], 'result': result})
if __name__ == '__main__':
    main()
