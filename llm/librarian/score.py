#!/usr/bin/env python3
"""Score the librarian's answers against this section's key.

Usage:
  python3 llm/librarian/score.py ANSWERS [--key KEY]

ANSWERS is the librarian's final message, saved to a file. Each answer begins
"A<n>:" (run.md asks for that form) and runs to the next one. The key's table
gives each question's Must hold column: patterns separated by " ; ", each a
regular expression (case ignored) the answer must contain; "|" inside one
separates alternatives. An answer is right when it holds every pattern. Prints
each answer right or wrong with the patterns it lacks, then the score. The pass:
7 of 8 right and both "not in the notes" answers right. Exits 0 on a pass.
"""
import argparse, os, re, sys

ROW = re.compile(r'^\|\s*(\d+)\s*\|(.*)\|\s*([^|]*)\|\s*$')


def load_key(path):
    key = {}
    for line in open(path, encoding='utf-8'):
        m = ROW.match(line.replace('\\|', '\x00'))
        if m:
            pats = [p.strip().strip('`').replace('\x00', '|') for p in m.group(3).split(';') if p.strip()]
            key[int(m.group(1))] = pats
    return key


def answers(path):
    out, cur = {}, None
    for line in open(path, encoding='utf-8'):
        m = re.match(r'^\s*(?:[-*]\s*)?\**A(\d+)\**\s*[:.]', line)
        if m:
            cur = int(m.group(1))
            out[cur] = line
        elif cur is not None:
            out[cur] += line
    return out


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument('answers')
    ap.add_argument('--key', default=os.path.join(here, 'answers.md'))
    a = ap.parse_args()
    key, got = load_key(a.key), answers(a.answers)
    right, nin_ok = 0, True
    for q, pats in sorted(key.items()):
        text = got.get(q, '')
        lack = [p for p in pats if not re.search(p, text, re.I)]
        ok = bool(text) and not lack
        right += ok
        if any('not in the notes' in p for p in pats) and not ok:
            nin_ok = False
        print(f"{'right' if ok else 'WRONG'}  Q{q}" + ('' if ok else f": lacks {lack}" if text else ': no answer'))
    need = len(key) - 1
    ok = right >= need and nin_ok
    print(f'\n{right} of {len(key)} right; pass needs {need} and both "not in the notes": {"PASS" if ok else "FAIL"}')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
