"""Small task-oriented CLI; old commands remain available."""
import argparse
from . import generator
from .catalog import get_family, load_families
from .files import read_json, read_rows, write, write_bundle


def parser():
    root=argparse.ArgumentParser(description='Preview families, prepare study inputs, and export review samples.')
    commands=root.add_subparsers(dest='command',required=True)
    commands.add_parser('list',help='List family IDs and contexts.')
    preview=commands.add_parser('preview',help='See sample problems without writing a dataset.')
    preview.add_argument('family',help='Probe family ID, for example F01.')
    preview.add_argument('--seed',default='preview-v0')
    preview.add_argument('--count',type=int,default=3)
    preview.add_argument('--history',action='store_true')
    review=commands.add_parser('review',help='Write a Markdown review pack for the committee.')
    review.add_argument('output'); review.add_argument('--samples',type=int,default=5)
    review.add_argument('--seed',default='committee-review-v0')
    for command in ('prepare','generate'):
        cmd=commands.add_parser(command,help='Prepare raw + runner files together.' if command=='prepare' else 'Generate raw probe JSONL only.')
        cmd.add_argument('split',choices=generator.SPLITS)
        cmd.add_argument('output'); cmd.add_argument('--seed',required=True)
        cmd.add_argument('--registration',help='Actual preregistration record (required for confirmation).')
    families=commands.add_parser('families',help='Export family definitions and freeze hashes.')
    families.add_argument('output')
    for command in ('histories','collisions'):
        cmd=commands.add_parser(command)
        cmd.add_argument('input'); cmd.add_argument('output')
        if command=='collisions':
            cmd.add_argument('--registration',help='Required when replacing confirmatory probes.')
    adapter=commands.add_parser('export-harness',help='Export existing raw files to task 3, including replacements.')
    adapter.add_argument('probes'); adapter.add_argument('histories'); adapter.add_argument('directory')
    return root


def run(args):
    if args.command=='list':
        for family in load_families():
            print(f"{family.family_id}  {family.probe.domain} -> {family.history_family_id}: {family.history.domain}"+
                  (' [held out]' if family.heldout else ''))
    elif args.command=='preview':
        if not 1 <= args.count <= 100:
            raise ValueError('Choose between 1 and 100 preview samples.')
        family=get_family(args.family)
        for index in range(args.count):
            row=family.generate(seed=args.seed,index=index,history=args.history)
            print(f"\n{row['item_id']}\n{row['problem']}\nIntermediate values: {row['intermediate_values']}\nFinal answer: {row['final_answer']}")
    elif args.command=='review':
        from .review import export_review
        export_review(args.output,args.samples,args.seed)
        print(f'Review-only examples saved to {args.output}.')
    elif args.command in ('prepare','generate'):
        registration=read_json(args.registration) if args.registration else None
        if args.command=='prepare':
            from .workflow import prepare
            probes,histories=prepare(args.split,args.seed,args.output,registration)
            print(f'Prepared {probes} probes and {histories} history problems in {args.output}.')
            print('Use items.jsonl and history_items.jsonl with task 3. History collision checks remain pending.')
        else:
            write(args.output,generator.generate(args.split,args.seed,registration),True)
    elif args.command=='families':
        write(args.output,{'families':generator.families(),'definitions':[f.describe() for f in load_families()],
                          'family_hash':generator.digest(generator.families()),'generator_hash':generator.source_hash(),
                          'paraphrases':generator.PARAPHRASES})
    elif args.command=='histories':
        write(args.output,generator.generate_histories(read_rows(args.input)),True)
    elif args.command=='collisions':
        registration=read_json(args.registration) if args.registration else None
        write(args.output,[generator.replace_collision(row['probe'],row['histories'],registration=registration) for row in read_rows(args.input)],True)
    elif args.command=='export-harness':
        from .harness_export import export
        probes,histories=export(read_rows(args.probes),read_rows(args.histories))
        write_bundle(args.directory,{'items.jsonl':(probes,True),'history_items.jsonl':(histories,True)},
                     {'generator_hash':generator.source_hash(),'probe_count':len(probes),'history_count':len(histories)})


def main():
    cli=parser()
    args=cli.parse_args()
    try:
        run(args)
    except KeyError as exc:
        cli.error(f'Missing required field: {exc.args[0]}. See README.md for the input format.')
    except (ValueError,OSError) as exc:
        cli.error(str(exc))


if __name__=='__main__':
    main()
