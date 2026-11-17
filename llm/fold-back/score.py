#!/usr/bin/env python3
"""Score a fold-back run against this section's key (checks R1 to R13).

Usage:
  python3 llm/fold-back/score.py [--book runs/fold-back/book] [--report runs/fold-back/report.md]

BOOK is the scratch copy the run edited (run.md makes it). The checks are the
key's Required table: the prose untouched, the Next pass list last in the notes,
its backticked quotes resolving in the prose (the kit's tools/quotes.py, found
by WSS_KIT, else ../world-saga-seed or ../story-kit beside this repo), the drift,
beat and held items, the folded window beat, settled lines kept, the open item
answered, marks on added lines, nothing struck, and the report's head. Paths
default to the run.md paths from the top of this repo. Exits 0 on a pass.
"""
import argparse, difflib, os, pathlib, re, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
SLUG = '00400-the-forty-minutes.md'
MARK = re.compile(r'\((?:Proposal|Answered|Settled|Aim|Resolved)')


def kit():
    env = os.environ.get('WSS_KIT')
    for c in ([env] if env else []) + [REPO.parent / 'world-saga-seed', REPO.parent / 'story-kit']:
        if c and (pathlib.Path(c) / 'tools' / 'quotes.py').exists():
            return pathlib.Path(c)
    sys.exit('kit not found: set WSS_KIT to the kit folder')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--book', default=str(REPO / 'runs' / 'fold-back' / 'book'))
    ap.add_argument('--report', default=str(REPO / 'runs' / 'fold-back' / 'report.md'))
    a = ap.parse_args()
    book = pathlib.Path(a.book)
    prose_p = book / 'story' / 'prose' / SLUG
    prose = prose_p.read_text(encoding='utf-8')
    outline = (book / 'story' / 'outline' / SLUG).read_text(encoding='utf-8')
    notes = (book / 'story' / 'notes' / SLUG).read_text(encoding='utf-8')
    orig_outline = (REPO / 'book' / 'story' / 'outline' / SLUG).read_text(encoding='utf-8')
    orig_notes = (HERE / 'notes.md').read_text(encoding='utf-8')
    results = []

    def check(rid, ok, what):
        results.append(ok)
        print(f"{'ok  ' if ok else 'FAIL'}  {rid} {what}")

    check('R1', prose == (HERE / 'prose.md').read_text(encoding='utf-8'), 'prose unchanged')
    heads = re.findall(r'^## (.+)$', notes, re.M)
    check('R2', bool(heads) and heads[-1].strip() == 'Next pass', f'last notes section: {heads[-1] if heads else None!r}')
    np = notes.split('## Next pass', 1)[1] if '## Next pass' in notes else ''
    tmp = tempfile.NamedTemporaryFile('w', suffix='.md', delete=False, encoding='utf-8')
    tmp.write(np); tmp.close()
    r = subprocess.run([sys.executable, str(kit() / 'tools' / 'quotes.py'), tmp.name, '--in', str(prose_p), '--backticks'],
                       capture_output=True, text=True)
    os.unlink(tmp.name)
    check('R3', r.returncode == 0, 'Next pass quotes resolve: ' + (r.stdout.strip().split('\n')[-1] if r.stdout.strip() else r.stderr.strip()))
    items = re.split(r'\n(?=\s*\d+\.\s|\s*[-*]\s)', np)

    def item(*pats):
        return any(all(re.search(p, it, re.I | re.S) for p in pats) for it in items)

    check('R4', item(r'drift', r'`[^`]*second post[^`]*`'), 'drift item quoting the second post')
    check('R5', item(r'\bbeat\b', r'apron'), 'beat item naming the apron')
    check('R6', item(r'\bheld\b', r'`[^`]*did not tell her that either[^`]*`'), 'held item quoting the closing line')
    check('R7', any('(Proposal, from the draft' in l and 'window' in l and '../prose/00400-the-forty-minutes.md' in l
                    for l in outline.split('\n')), 'window beat folded, marked and linked')
    check('R8', 'gallery bench' not in outline, '"gallery bench" deleted from the outline')
    settled = [l for l in orig_outline.split('\n') if '(Settled' in l]
    lost = [l for l in settled if l not in outline.split('\n')]
    check('R9', not lost, f'{len(settled) - len(lost)} of {len(settled)} settled lines kept' + (f'; lost: {lost[0][:60]}' if lost else ''))
    check('R10', any('(Answered by the draft' in l and 'skirt' in l for l in notes.split('\n'))
          and 'skirt or her apron?' not in notes, 'open item answered by the draft')
    unmarked = []
    for old, new in ((orig_outline, outline), (orig_notes, notes)):
        for l in difflib.ndiff(old.split('\n'), new.split('\n')):
            if l.startswith('+ ') and re.match(r'^\s*(?:[-*]|\d+\.)\s', l[2:]) and not MARK.search(l):
                unmarked.append(l[2:])
    check('R11', not unmarked, 'every added list line marked' + (f'; unmarked: {unmarked[0][:60]}' if unmarked else ''))
    check('R12', '~~' not in outline + notes, 'nothing struck')
    rep = pathlib.Path(a.report)
    first = rep.read_text(encoding='utf-8').split('\n', 1)[0].strip() if rep.exists() else None
    check('R13', first == '# Fold-back, 00400', f'report head: {first!r}')
    n = sum(results)
    print(f'\n{n} of {len(results)} required: {"PASS" if n == len(results) else "FAIL"}')
    sys.exit(0 if n == len(results) else 1)


if __name__ == '__main__':
    main()
