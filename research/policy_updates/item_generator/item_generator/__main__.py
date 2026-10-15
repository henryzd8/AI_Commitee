import argparse
import json
from pathlib import Path
from . import generator

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
    commands = parser.add_subparsers(dest='command', required=True)
    g = commands.add_parser('generate')
    g.add_argument('split', choices=['screening', 'exploration', 'manipulation', 'validation', 'confirmatory'])
    g.add_argument('output')
    g.add_argument('--seed', required=True)
    g.add_argument('--registration')
    f = commands.add_parser('families')
    f.add_argument('output')
    h = commands.add_parser('histories')
    h.add_argument('input')
    h.add_argument('output')
    c = commands.add_parser('collisions')
    c.add_argument('input')
    c.add_argument('output')
    args = parser.parse_args()
    if args.command == 'generate':
        result = generator.generate(args.split, args.seed, read(args.registration) if args.registration else None)
        write(args.output, result, True)
    elif args.command == 'families':
        write(args.output, {'families': generator.families(), 'family_hash': generator.digest(generator.families()), 'generator_hash': generator.source_hash(), 'paraphrases': generator.PARAPHRASES})
    elif args.command == 'histories':
        probes = rows(args.input)
        result = []
        for p in probes:
            for turn in range(4):
                r = generator.instance(int(p['family_id'][1:]) - 1, p['split'] + '-history', p['seed'] + ':' + p['item_id'], turn, True)
                result.append({**r, 'probe_item_id': p['item_id'], 'history_turn': turn + 1})
        write(args.output, result, True)
    elif args.command == 'collisions':
        write(args.output, [generator.replace_collision(r['probe'], r['histories']) for r in rows(args.input)], True)
if __name__ == '__main__':
    main()
