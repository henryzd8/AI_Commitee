"""Human-readable review-only examples for any registered template strategy."""
from pathlib import Path
from .catalog import load_families


def render_review(samples=5, seed='committee-review-v0'):
    if not 1 <= samples <= 100:
        raise ValueError('Choose between 1 and 100 review samples per family.')
    lines=['# Candidate family review pack','',
           'Unapproved development templates. A family is a reusable structure with varying numbers.',
           'Held-out families may be reviewed for quality but must not be used to tune prompts.','',
           '## Review checklist','',
           '- Is the wording clear and are quantities/units meaningful?',
           '- Re-solve the examples: are the intermediate values and final answer correct?',
           '- Are there 3–5 meaningful steps, or do operations cancel or collapse?',
           '- Does this require different reasoning from other families, beyond changed nouns?',
           '- Is the history family different from its probe family in context and operations?',
           '- Is the final answer absent from the question and intermediate values?',
           '', 'Record keep / revise / replace, reviewer initials, and reasons for every pair.',
           'These inventory candidates remain mechanically similar; software structure does not establish independent families.','']
    for family in load_families():
        lines += [f'## {family.family_id} / {family.history_family_id}',
                  f"{'Held out from prompt development.' if family.heldout else 'Development family.'}",
                  '', '**Decision:** unreviewed · **Reviewer:** ______ · **Reason:** ______','']
        for history in (False,True):
            template=family.history if history else family.probe
            lines += [f"### {'History' if history else 'Probe'}: {template.domain}",'']
            for index in range(samples):
                row=family.generate(split='review-only',seed=seed,index=index,history=history)
                lines += [f"**Sample {index+1}.** {row['problem']}",'',
                          f"Intermediate values: {', '.join(map(str,row['intermediate_values'].values()))}. **Final answer: {row['final_answer']}.**",'']
    return '\n'.join(lines).rstrip()+'\n'


def export_review(path,samples=5,seed='committee-review-v0'):
    text=render_review(samples,seed)
    target=Path(path)
    target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('x',encoding='utf-8') as stream:
        stream.write(text)
