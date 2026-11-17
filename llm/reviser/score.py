#!/usr/bin/env python3
"""Score a revised 00400 against this section's key.

Usage:
  python3 llm/reviser/score.py REVISED [--key KEY] [--keep KEEP]

Checks: each fault text in answers.md's Gone table is no longer in the file; every
quote in keep.md still is (the kit's tools/quotes.py, found by WSS_KIT, else
../world-saga-seed or ../story-kit beside this repo); the title line is
unchanged. Matching ignores spacing, curly quotes and markdown emphasis, as
quotes.py does. Also prints the kit's tells.py banned-word count, not scored.
Exits 0 on a pass.
"""
import argparse, os, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent


def kit():
    env = os.environ.get('WSS_KIT')
    for c in ([env] if env else []) + [REPO.parent / 'world-saga-seed', REPO.parent / 'story-kit']:
        if c and (pathlib.Path(c) / 'tools' / 'quotes.py').exists():
            return pathlib.Path(c)
    sys.exit('kit not found: set WSS_KIT to the kit folder')


def norm(s):
    s = s.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
    s = re.sub(r'[*_]', '', s)
    return re.sub(r'\s+', ' ', s).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('revised')
    ap.add_argument('--key', default=str(HERE / 'answers.md'))
    ap.add_argument('--keep', default=str(HERE / 'keep.md'))
    a = ap.parse_args()
    key = open(a.key, encoding='utf-8').read()
    gone = re.findall(r'^\|\s*(F\d+)\s*\|\s*\d+\s*\|\s*`([^`]+)`', key, re.M)
    title = re.search(r'^The first line unchanged: `([^`]+)`', key, re.M).group(1)
    text = open(a.revised, encoding='utf-8').read()
    fails = 0
    for fid, t in gone:
        ok = norm(t) not in norm(text)
        fails += not ok
        print(f"{'gone' if ok else 'STILL'}  {fid}: {t}")
    k = kit()
    r = subprocess.run([sys.executable, str(k / 'tools' / 'quotes.py'), a.keep, '--in', a.revised, '-v'],
                       capture_output=True, text=True)
    print(r.stdout.rstrip())
    fails += r.returncode != 0
    first = text.split('\n', 1)[0].strip()
    ok = first == title
    fails += not ok
    print(f"{'title ok' if ok else 'TITLE CHANGED'}: {first!r}")
    t = subprocess.run([sys.executable, str(k / 'tools' / 'tells.py'), a.revised,
                        '--banned', str(REPO / 'book' / 'story' / 'voice' / 'banned.txt')],
                       capture_output=True, text=True).stdout
    print('info  ' + t.strip().split('\n')[0])
    m = re.search(r'(\d+) banned-word hits', t)
    print(f'info  banned-word hits: {m.group(1) if m else "?"} (not scored)')
    print(f'\n{fails} checks failed: {"PASS" if fails == 0 else "FAIL"}')
    sys.exit(0 if fails == 0 else 1)


if __name__ == '__main__':
    main()
