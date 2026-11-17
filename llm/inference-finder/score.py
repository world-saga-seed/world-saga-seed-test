#!/usr/bin/env python3
"""Score an inference-finder report: llm/score.py, plus the near-miss check.

Usage:
  python3 llm/inference-finder/score.py REPORT [--slack N]

Runs the shared scorer (llm/score.py) on this section's answers.md: a plant is caught
when any finding names its line. A finder lists every inference, so unmatched
findings are expected and not capped. Then the near misses (answers.md, "Grounded near
misses"): each is grounded a line earlier, so the finder should list it WITH that
evidence. A finding on a near miss's line that says "none on the page" is an error.
The pass needs the key's pass line and no near-miss errors. Exits 0 on a pass.
"""
import importlib.util, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('score', os.path.join(HERE, '..', 'score.py'))
base = importlib.util.module_from_spec(spec); spec.loader.exec_module(base)
NEAR = re.compile(r'^\|\s*(N\d+)\s*\|\s*(\d+)\s*\|')


def near_misses(key):
    return [(m.group(1), int(m.group(2))) for m in map(NEAR.match, open(key, encoding='utf-8')) if m]


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    key = os.path.join(HERE, 'answers.md')
    slack = int(args[args.index('--slack') + 1]) if '--slack' in args else 1
    r = subprocess.run([sys.executable, os.path.join(HERE, '..', 'score.py'), key, *args])
    errors = 0
    for nid, n in near_misses(key):
        for i, ln, text in base.findings(args[0]):
            if abs(ln - n) <= slack and re.search(r'none on the page', text, re.I):
                errors += 1
                print(f'NEAR-MISS ERROR  {nid} line {n}: listed with "none on the page" (report:{i})')
    print(f'{errors} near-miss errors: {"PASS" if r.returncode == 0 and errors == 0 else "FAIL"}')
    sys.exit(0 if r.returncode == 0 and errors == 0 else 1)


if __name__ == '__main__':
    main()
