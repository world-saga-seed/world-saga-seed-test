#!/usr/bin/env python3
"""Score a prompt's report against a section's answer key.

Usage:
  python3 llm/score.py llm/<section>/answers.md REPORT [--slack N]

The key is a markdown table, one row per planted fault:

  | ID | Line | Kind | Plant |
  |---|---|---|---|
  | K1 | 23 | fact | the tide given as six against the table's seven |
  | K2 | 40-42 | voice | a word the narrator would not use |

A sixth cell, Must, is optional: a regex the finding's text (the item and what
is indented under it) has to contain to count, for a line where a finding on
something else could be scored as the catch. Leave it empty to match by line. Write a pipe in it as \\|.

A line "**Input:** PATH" in the key names the file the prompt read (by default
chapter.md, outline.md or inventions.md beside the key). A finding that quotes
four words or more found on a plant's lines then catches it whatever line it
cites, since models miscount lines.

and a pass line above or below it:

  **Pass:** 4 of 5 caught, at most 1 unmatched.

The report is what the prompt wrote. Every finding the prompt makes names its
line ("line 23", "L23", ":23"; the section's run.md asks for that). A finding is one
top-level list item with whatever is indented under it, scored at the first
line it names, so its "against" quote of another file is not counted. A finding
catches a plant when its line is within --slack lines (default 1) of the plant's
line or range. A finding near no plant is "unmatched": it is either invented or
a real fault the key does not hold, so read each one before you call it an
invention, and if it is real, add it to the key.

Prints each plant caught or missed, each unmatched finding, the score, and
PASS or FAIL against the pass line. Exits 0 on a pass, 1 on a fail.
"""
import argparse, re, sys

PASS = re.compile(r'\*\*Pass:\*\*\s*(\d+)\s+of\s+(\d+)\s+caught(?:,\s*at most\s+(\d+)\s+unmatched)?', re.I)
LINE = re.compile(r'(?:\bline\s+|\bL|:)(\d{1,4})\b', re.I)


def cells(line):
    """A table row's cells, split on pipes not escaped as \\|."""
    parts = re.split(r'(?<!\\)\|', line.strip())
    return [c.replace('\\|', '|').strip() for c in parts[1:-1]]


def load_key(path):
    plants, need, most = [], None, None
    for line in open(path, encoding='utf-8'):
        c = cells(line) if line.lstrip().startswith('|') else []
        if len(c) >= 4 and re.fullmatch(r'K\d+', c[0]):
            r = re.fullmatch(r'(\d+)(?:\s*-\s*(\d+))?', c[1])
            if r:
                a = int(r.group(1))
                must = c[4].strip('`') if len(c) > 4 else ''
                plants.append((c[0], a, int(r.group(2) or a), c[2], c[3], re.compile(must, re.I) if must else None))
        p = PASS.search(line)
        if p:
            need, most = int(p.group(1)), (int(p.group(3)) if p.group(3) is not None else None)
    return plants, need, most


def findings(path):
    """(report line number, line number named, text) for each finding.

    A finding is a top-level list item (not indented), with any indented lines
    under it; it is scored at the first line number it names, so a sub-item
    quoting the other file's line ("against: page.md line 7") is not a finding
    of its own."""
    items, cur = [], None
    for i, line in enumerate(open(path, encoding='utf-8'), 1):
        top = re.match(r'^(?:[-*]|\d+\.)\s', line)
        if top:
            cur = [i, line.strip(), [line]]
            items.append(cur)
        elif cur and line.strip() and (line[:1].isspace() or re.match(r'^\s*[-*]\s', line)):
            cur[2].append(line)
        elif not line.strip():
            continue
        else:
            cur = None
    out = []
    for i, text, lines in items:
        for l in lines:
            m = LINE.search(l)
            if m:
                out.append((i, int(m.group(1)), ' '.join(x.strip() for x in lines)))
                break
    return out


QUOTE = re.compile(r'"([^"]{12,})"|“([^”]{12,})”|`([^`]{12,})`')


def norm(s):
    s = s.replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'")
    return ' '.join(re.sub(r'[*_]', '', s).split()).lower()


def input_lines(key):
    import os
    t = open(key, encoding='utf-8').read()
    m = re.search(r'\*\*Input:\*\*\s*`?([^`\s]+)`?', t)
    here = os.path.dirname(os.path.abspath(key))
    cands = [m.group(1)] if m else [os.path.join(here, n) for n in ('chapter.md', 'outline.md', 'inventions.md')]
    for c in cands:
        for p in (c, os.path.join(os.path.dirname(here), '..', c), os.path.join(here, os.path.basename(c))):
            if os.path.exists(p):
                return [norm(l) for l in open(p, encoding='utf-8').read().split('\n')]
    return []


def quoted_on(body, lines, lo, hi, cited):
    """Does the finding quote four words or more found on lines lo..hi, and not on the line it cites?
    A quote that is also on its cited line means the finding is about that line."""
    span = ' '.join(lines[max(0, lo - 1):hi])
    own = lines[cited - 1] if 0 < cited <= len(lines) else ''
    for m in QUOTE.finditer(body):
        words = norm(next(g for g in m.groups() if g)).split()
        runs = [' '.join(words[i:i + 4]) for i in range(len(words) - 3)]
        if any(r in span for r in runs) and not any(r in own for r in runs):
            return True
    return False


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
    lines = input_lines(a.key)
    caught, used, by_quote = set(), set(), set()
    for pid, lo, hi, kind, text, must in plants:
        for j, (_, n, body) in enumerate(found):
            near = lo - a.slack <= n <= hi + a.slack
            if (near or (lines and quoted_on(body, lines, lo, hi, n))) and (must is None or must.search(body)):
                caught.add(pid)
                used.add(j)
                if not near:
                    by_quote.add(pid)
    for pid, lo, hi, kind, text, must in plants:
        where = f'{lo}' if lo == hi else f'{lo}-{hi}'
        print(f"{'caught' if pid in caught else 'MISSED'}  {pid} line {where} ({kind}): {text}"
              + ('  [by quote: the finding cites another line]' if pid in by_quote else ''))
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
