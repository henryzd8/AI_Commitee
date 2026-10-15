"""Export review-only samples, never confirmatory stimuli. No overwrites."""
from pathlib import Path
from item_generator.generator import families, instance

lines=['# Candidate family review pack',
       '', 'These are **unapproved candidate templates**, not finalized study families.',
       'A family keeps a problem structure fixed while changing the numerical inputs.',
       'F01–F40 are probe families; H01–H40 supply their paired history problems.',
       'F33–F40 are held out from prompt development. Review them for quality, but do not use their examples to tune prompts.',
       '', '## What to review', '',
       '1. **Clear meaning:** Is the wording unambiguous? Do units and operations make sense? These initial inventory exercises may need more natural stories.',
       '2. **Correct arithmetic:** Re-solve the samples and check the named steps and final answer. Automated agreement is not independent human approval.',
       '3. **Actual difficulty:** Does solving it require the intended 3–5 meaningful steps? Can steps cancel, merge, or make the problem trivial?',
       '4. **Family diversity:** Compare other families. Different nouns or operation orders do not automatically mean different reasoning structures or independent statistical clusters.',
       '5. **Probe/history distinction:** Does the paired history use a genuinely different context and operation sequence while remaining comparable in difficulty?',
       '6. **No answer leakage:** The final number must not appear in the question or among intermediate values. Look for wording that gives it away even without printing it.',
       '', 'For each pair record **keep / revise / replace**, the reason, and reviewer initials. All entries below start unreviewed.',
       '', 'The current generator often gives explicit arithmetic instructions in an inventory setting. Treat this as an engineering starting point, not a claim that these are 40 rich natural-language word-problem types.',
       '', '## Index', '', '| Probe | Context | Operations | History | Context | Operations |', '|---|---|---|---|---|---|']
for f in families():
    lines.append(f"| [{f['family_id']}](#{f['family_id'].lower()}--{f['history_family_id'].lower()}) | {f['domain']} | {' → '.join(f['operations'])} | {f['history_family_id']} | {f['history_domain']} | {' → '.join(f['history_operations'])} |")
for i,f in enumerate(families()):
    lines += ['',f"## {f['family_id']} / {f['history_family_id']}",'',
              '**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______','']
    for history in (False,True):
        lines += [f"### {'History' if history else 'Probe'}: {f['history_domain' if history else 'domain']}",'']
        for j in range(5):
            item=instance(i,'review-only','committee-review-v0',j,history)
            lines += [f"**Sample {j+1}.** {item['problem']}",'',
                      f"Steps: {', '.join(str(v) for v in item['intermediate_values'].values())}. **Final answer: {item['final_answer']}.**",'']
with Path('FAMILY_REVIEW.md').open('x',encoding='utf-8') as stream:
    stream.write('\n'.join(lines)+'\n')
print('Exported 400 review-only samples across 80 candidate families.')
