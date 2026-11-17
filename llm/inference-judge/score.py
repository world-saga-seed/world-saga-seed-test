#!/usr/bin/env python3
"""Score an inference-judge report: its Breaks section only, plus the near-miss check.

Usage:
  python3 llm/inference-judge/score.py REPORT [--slack N]

The judge sorts every find into breaks, known from before, and questions. Only a
break is a finding, so this copies the report's Breaks section (from a heading or
bold line holding "Breaks" to the next heading or bold section label) to a scratch
file and runs the shared scorer (llm/score.py) on it with this section's answers.md.
A break on a near miss's line (answers.md, "Grounded near misses") is an error: the
grounds are on the page a line earlier. The pass needs the key's pass line and no
near-miss errors. Plants the judge sent to Questions are listed as "softened" for
the reader of the score; they count as missed. Exits 0 on a pass.
"""
import importlib.util, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('score', os.path.join(HERE, '..', 'score.py'))
base = importlib.util.module_from_spec(spec); spec.loader.exec_module(base)
NEAR = re.compile(r'^\|\s*(N\d+)\s*\|\s*(\d+)\s*\|')
LABEL = re.compile(r'^\s*(?:#+\s*|[-*]\s*)?\*\*([^*]+)\*\*|^\s*#+\s*(.+)$')


def sections(path):
    """{section label: [lines]}, by headings and bold labels."""
    out, cur = {}, None
    for line in open(path, encoding='utf-8'):
        m = LABEL.match(line)
        if m:
            label = (m.group(1) or m.group(2) or '').lower()
            for name in ('breaks', 'known from before', 'questions', 'tally'):
                if name in label:
                    cur = name
                    break
            else:
                if line.lstrip().startswith('#'):
                    cur = None
        if cur:
            out.setdefault(cur, []).append(line)
    return out


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    key = os.path.join(HERE, 'answers.md')
    slack = int(args[args.index('--slack') + 1]) if '--slack' in args else 1
    secs = sections(args[0])
    if 'breaks' not in secs:
        print('no Breaks section found: scoring the whole report')
        breaks = open(args[0], encoding='utf-8').read()
    else:
        breaks = ''.join(secs['breaks'])
    tmp = tempfile.NamedTemporaryFile('w', suffix='.md', delete=False, encoding='utf-8')
    tmp.write(breaks); tmp.close()
    r = subprocess.run([sys.executable, os.path.join(HERE, '..', 'score.py'), key, tmp.name, *args[1:]])
    errors = 0
    for nid, n in [(m.group(1), int(m.group(2))) for m in map(NEAR.match, open(key, encoding='utf-8')) if m]:
        for i, ln, text in base.findings(tmp.name):
            if abs(ln - n) <= slack:
                errors += 1
                print(f'NEAR-MISS ERROR  {nid} line {n}: called a break: {text[:100]}')
    if 'questions' in secs:
        q = tempfile.NamedTemporaryFile('w', suffix='.md', delete=False, encoding='utf-8')
        q.write(''.join(secs['questions'])); q.close()
        plants, _, _ = base.load_key(key)
        for i, ln, text in base.findings(q.name):
            for pid, lo, hi, kind, plant, *_ in plants:
                if lo - slack <= ln <= hi + slack:
                    print(f'softened  {pid} line {lo}: sent to Questions, not Breaks')
        os.unlink(q.name)
    os.unlink(tmp.name)
    ok = r.returncode == 0 and errors == 0
    print(f'{errors} near-miss errors: {"PASS" if ok else "FAIL"}')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
