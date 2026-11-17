#!/usr/bin/env python3
"""Score a prompt's report against a section's answer key.

Usage:
  python3 llm/score.py llm/<section>/key.md REPORT [--slack N]

The key is a markdown table, one row per planted fault:

  | ID | Line | Kind | Plant |
  |---|---|---|---|
  | K1 | 23 | fact | the tide given as six against the table's seven |
  | K2 | 40-42 | voice | a word the narrator would not use |

and a pass line above or below it:

  **Pass:** 4 of 5 caught, at most 1 unmatched.

The report is what the prompt wrote. Every finding the prompt makes names its
line ("line 23", "L23", ":23"; the section's run.md asks for that). A finding
catches a plant when its line is within --slack lines (default 1) of the plant's
line or range. A finding near no plant is "unmatched": it is either invented or
a real fault the key does not hold, so read each one before you call it an
invention, and if it is real, add it to the key.

Prints each plant caught or missed, each unmatched finding, the score, and
PASS or FAIL against the pass line. Exits 0 on a pass, 1 on a fail.
"""
import argparse, re, sys

ROW = re.compile(r'^\|\s*(K\d+)\s*\|\s*(\d+)(?:\s*-\s*(\d+))?\s*\|\s*([^|]*)\|\s*([^|]*)\|')
PASS = re.compile(r'\*\*Pass:\*\*\s*(\d+)\s+of\s+(\d+)\s+caught(?:,\s*at most\s+(\d+)\s+unmatched)?', re.I)
LINE = re.compile(r'(?:\bline\s+|\bL|:)(\d{1,4})\b', re.I)


def load_key(path):
    plants, need, most = [], None, None
    for line in open(path, encoding='utf-8'):
        m = ROW.match(line)
        if m:
            a = int(m.group(2))
            plants.append((m.group(1), a, int(m.group(3) or a), m.group(4).strip(), m.group(5).strip()))
        p = PASS.search(line)
        if p:
            need, most = int(p.group(1)), (int(p.group(3)) if p.group(3) is not None else None)
    return plants, need, most


def findings(path):
    """(report line number, first line number named, text) for each finding: a list item naming a line."""
    out = []
    for i, line in enumerate(open(path, encoding='utf-8'), 1):
        if not re.match(r'^\s*(?:[-*]|\d+\.)\s', line):
            continue
        m = LINE.search(line)
        if m:
            out.append((i, int(m.group(1)), line.strip()))
    return out


def main():
    ap = argparse.ArgumentParser(description="Score a prompt's report against a section's key.")
    ap.add_argument('key')
    ap.add_argument('report')
    ap.add_argument('--slack', type=int, default=1)
    a = ap.parse_args()
    plants, need, most = load_key(a.key)
    if not plants:
        sys.exit(f'no plants in {a.key}')
    found = findings(a.report)
    caught, used = set(), set()
    for pid, lo, hi, kind, text in plants:
        for j, (_, n, _) in enumerate(found):
            if lo - a.slack <= n <= hi + a.slack:
                caught.add(pid)
                used.add(j)
    for pid, lo, hi, kind, text in plants:
        where = f'{lo}' if lo == hi else f'{lo}-{hi}'
        print(f"{'caught' if pid in caught else 'MISSED'}  {pid} line {where} ({kind}): {text}")
    unmatched = [f for j, f in enumerate(found) if j not in used]
    for i, n, text in unmatched:
        print(f'unmatched  report:{i} (line {n}): {text[:120]}')
    need = need if need is not None else len(plants)
    ok = len(caught) >= need and (most is None or len(unmatched) <= most)
    print(f'\n{len(caught)} of {len(plants)} caught, {len(unmatched)} unmatched; '
          f'pass needs {need}' + (f' and at most {most} unmatched' if most is not None else '') +
          f': {"PASS" if ok else "FAIL"}')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
