#!/usr/bin/env python3
"""Score a drafted 00700 against this section's key.

Usage:
  python3 llm/drafter/score.py DRAFT [--report REPORT] [--key KEY]

Checks, from answers.md: each beat's must-have patterns in the draft; 0 banned-word
hits in narration and the texture bands, both from the kit's tools/tells.py
(found by WSS_KIT, else ../world-saga-seed or ../story-kit beside this repo);
the title line; and with --report, the drafter's report lists inventions and
leaves Agnes's answer open. Prints each check and PASS or FAIL. Exits 0 on a pass.
"""
import argparse, os, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent


def kit():
    env = os.environ.get('WSS_KIT')
    for c in ([env] if env else []) + [REPO.parent / 'world-saga-seed', REPO.parent / 'story-kit']:
        if c and (pathlib.Path(c) / 'tools' / 'tells.py').exists():
            return pathlib.Path(c)
    sys.exit('kit not found: set WSS_KIT to the kit folder')


def key_tables(path):
    beats, bands, title = [], {}, None
    for line in open(path, encoding='utf-8'):
        l = line.replace('\\|', '\x00')
        m = re.match(r'^\|\s*(\d+)\s*\|[^|]*\|\s*([^|]*)\|\s*$', l)
        if m and '`' in m.group(2):
            beats.append((int(m.group(1)), [p.strip().strip('`').replace('\x00', '|')
                                            for p in m.group(2).split(';') if p.strip()]))
        m = re.match(r'^\|\s*([a-z/]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|', line)
        if m:
            bands[m.group(1)] = (float(m.group(2)), float(m.group(3)))
        m = re.match(r'^The first line is exactly `([^`]+)`', line)
        if m:
            title = m.group(1)
    return beats, bands, title


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('draft')
    ap.add_argument('--report')
    ap.add_argument('--key', default=str(HERE / 'answers.md'))
    a = ap.parse_args()
    beats, bands, title = key_tables(a.key)
    text = open(a.draft, encoding='utf-8').read()
    fails = 0

    def check(ok, what):
        nonlocal fails
        fails += not ok
        print(f"{'ok  ' if ok else 'FAIL'}  {what}")

    for n, pats in beats:
        for p in pats:
            check(re.search(p, text, re.I) is not None, f'beat {n}: /{p}/')
    banned = REPO / 'book' / 'story' / 'voice' / 'banned.txt'
    out = subprocess.run([sys.executable, str(kit() / 'tools' / 'tells.py'), a.draft, '--banned', str(banned)],
                         capture_output=True, text=True).stdout
    print(out.rstrip())
    hits = re.search(r'(\d+) banned-word hits', out)
    check(hits is not None and int(hits.group(1)) == 0, f'banned hits: {hits.group(1) if hits else "?"}')
    nums = dict(re.findall(r'([a-z/]+)=\s*([\d.]+)', out.split('\n')[0]))
    for m, (lo, hi) in bands.items():
        v = float(nums[m]) if m in nums else None
        check(v is not None and lo <= v <= hi, f'{m} = {v} in {lo} to {hi}')
    first = text.split('\n', 1)[0].strip()
    check(first == title, f'title line: {first!r}')
    if 'w' in nums:
        print(f'info  narration words: {nums["w"]} (target 1,200 to 1,800; not scored)')
    if a.report:
        rep = open(a.report, encoding='utf-8').read()
        check(re.search(r'inventions', rep, re.I) is not None, 'report: an Inventions list')
        check(any(re.search(r'\bopen\b', l, re.I) and re.search(r'agnes|forty', l, re.I)
                  for l in rep.split('\n')), "report: Agnes's answer left open")
    print(f'\n{fails} checks failed: {"PASS" if fails == 0 else "FAIL"}')
    sys.exit(0 if fails == 0 else 1)


if __name__ == '__main__':
    main()
