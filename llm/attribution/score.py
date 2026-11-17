#!/usr/bin/env python3
"""Score an attribution-test report against this section's key.

Usage:
  python3 llm/attribution/score.py REPORT [--key KEY]

The key (answers.md) holds the kit's key lines, "- P1: file:line, Head", and a line
"**Planted:** P<n> ...", the paragraph written in the other head's voice.
The report gives each paragraph as a list item that begins "- P<n>: <Head>"
(or "either"; run.md asks for that form), then a closing paragraph.

A clean paragraph is right when the report's head is the key's. The planted one
is caught when the report gives it to the other head or "either", or when the
closing text names it (P<n>) in a sentence that says wrong, either, could
belong, bleed or slip. A clean paragraph called "either", or named so in the
closing text, is a false flag. The pass: 13 of 14 clean right, the plant caught,
at most 1 false flag. Exits 0 on a pass.
"""
import argparse, os, re, sys

KEYLINE = re.compile(r'^-\s*P(\d+):\s*[^,]+,\s*(\w+)')
PLANT = re.compile(r'\*\*Planted:\*\*\s*P(\d+)')
ITEM = re.compile(r'^\s*(?:[-*]|\d+\.)\s*\**P(\d+)\**\s*[:.\-–—]\s*\**\s*([A-Za-z]+)')
NEGATED = re.compile(r'\b(?:none|no|not|never|nothing)\b[^.;]*?\b(?:wrong|odd one)\b', re.I)
FLAGWORDS = re.compile(r'wrong|either|could belong|bleed|slip|out of (?:its|her) voice|odd one', re.I)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument('report')
    ap.add_argument('--key', default=os.path.join(here, 'answers.md'))
    a = ap.parse_args()
    key, plant = {}, None
    for line in open(a.key, encoding='utf-8'):
        m = KEYLINE.match(line)
        if m:
            key[int(m.group(1))] = m.group(2).lower()
        p = PLANT.search(line)
        if p:
            plant = int(p.group(1))
    heads = set(key.values())
    given, rest = {}, []
    for line in open(a.report, encoding='utf-8'):
        m = ITEM.match(line)
        if m and int(m.group(1)) not in given:
            given[int(m.group(1))] = m.group(2).lower()
        elif not m:
            rest.append(line)
    flagged = set()
    for sentence in re.split(r'(?<=[.!?])\s+', ' '.join(rest)):
        # a flag is a clause naming a paragraph and doubting it; "none seemed wrong" is not one
        for clause in re.split(r'[;,]|\band\b', sentence):
            if FLAGWORDS.search(NEGATED.sub('', clause)):
                flagged |= {int(n) for n in re.findall(r'\bP(\d+)\b', clause)}
    right, false_flags = 0, []
    for n in sorted(key):
        g = given.get(n, '(none)')
        if n == plant:
            caught = (g != key[n]) or n in flagged
            print(f"{'caught' if caught else 'MISSED'}  P{n} planted ({key[n]}'s head, the other voice): given {g}" +
                  (', named in closing' if n in flagged else ''))
            continue
        ok = g == key[n]
        right += ok
        flag = g == 'either' or n in flagged
        if flag:
            false_flags.append(n)
        print(f"{'right' if ok else 'WRONG'}  P{n} {key[n]}: given {g}" + (' (false flag)' if flag else ''))
    clean = len(key) - (1 if plant else 0)
    caught = plant is not None and ((given.get(plant, '(none)') != key[plant]) or plant in flagged)
    ok = right >= clean - 1 and caught and len(false_flags) <= 1
    print(f'\n{right} of {clean} clean right, plant {"caught" if caught else "missed"}, '
          f'{len(false_flags)} false flags; pass needs {clean - 1}, the plant, at most 1: {"PASS" if ok else "FAIL"}')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
