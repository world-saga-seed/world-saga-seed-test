"""aged.py: outline beats, and note and card lines, that may carry an old draft into a redraft.

The cases plant: a beat "from the draft"; a link to a sibling outline that shares
a retired draft's file name (not cited) beside a link that resolves to the retired
prose and a `prose/...:12` locator (both cited); dated lines either side of a
--cutoff; ruling IDs dated by a ledger file, two-part and three-part; open
proposals with and without a date or ruling; and the --beats, --cites-only and
--tsv options.
"""
import pytest
from conftest import run, write

OUTLINE = 'story/outline/00200-x.md'


def tree(tmp_path, outline, ledger=''):
    write(tmp_path, {
        OUTLINE: outline,
        'story/outline/00300-y.md': '# Y (outline)\n\n- The next chapter, kept as it is.\n',
        'story/prose/00300-y.md': '# Y\n\nThe old draft of the next chapter.\n',
        'plan/settled/ledger/2026-10-26.md': ledger or '| ID | Kind | Ruling |\n|---|---|---|\n',
    })
    return tmp_path


def rows(path):
    """{line number: reasons} from the --tsv file."""
    out = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        f, n, why, _ = line.split('\t', 3)
        out[int(n)] = why
    return out


CITES = """# X (outline)

- Sibling link: see [the next chapter](00300-y.md) for the turn at the ford.
- Retired link: [the old draft](../prose/00300-y.md) holds the gull scene.
- Locator: as in `prose/00300-y.md:12`, the gull on the post.
- A beat drawn from the draft of the old book.
Prose that came from the draft, not a list item.
1. A numbered beat with no marks at all.
"""


def test_smoke_on_book(book):
    code, out = run('aged', 'story/outline/00400-the-forty-minutes.md', 'story/outline/1-spring-tides.md',
                    '--retired', 'story/prose/00400-the-forty-minutes.md', cwd=book)
    assert code == 0
    assert 'lines flagged in 2 files' in out


def test_sibling_outline_is_not_retired_but_prose_link_and_locator_are(tmp_path):
    tree(tmp_path, CITES)
    code, out = run('aged', OUTLINE, '--retired', 'story/prose/00300-y.md', '--tsv', 'out.tsv', cwd=tmp_path)
    assert code == 0
    got = rows(tmp_path / 'out.tsv')
    assert 3 not in got                       # [..](00300-y.md): the sibling outline, not the draft
    assert got[4] == 'cites-retired'          # [..](../prose/00300-y.md) resolves to the retired draft
    assert got[5] == 'cites-retired'          # `prose/00300-y.md:12` names it as a locator
    assert got[6] == 'from-draft'
    assert got[7] == 'from-draft'
    assert 8 not in got
    assert f'{OUTLINE}: 6 lines, 4 flagged (cites-retired 2, from-draft 2)' in out
    assert '4 lines flagged in 1 files: cites-retired 2, from-draft 2' in out


def test_kept_draft_is_not_listed(tmp_path):
    tree(tmp_path, CITES)
    code, out = run('aged', OUTLINE, '--retired', 'story/prose/00999-other.md', '--tsv', 'out.tsv', cwd=tmp_path)
    assert code == 0
    assert 'cites-retired' not in out
    assert set(rows(tmp_path / 'out.tsv')) == {6, 7}


def test_beats_reads_only_list_items(tmp_path):
    tree(tmp_path, CITES)
    code, out = run('aged', OUTLINE, '--retired', 'story/prose/00300-y.md', '--beats', '--tsv', 'out.tsv', cwd=tmp_path)
    assert code == 0
    got = rows(tmp_path / 'out.tsv')
    assert 7 not in got                       # the prose line is not a beat
    assert got[6] == 'from-draft'
    assert f'{OUTLINE}: 5 lines, 3 flagged (cites-retired 2, from-draft 1)' in out


def test_cites_only_drops_from_draft(tmp_path):
    tree(tmp_path, CITES)
    code, out = run('aged', OUTLINE, '--retired', 'story/prose/00300-y.md', '--cites-only', '--tsv', 'out.tsv',
                    cwd=tmp_path)
    assert code == 0
    assert rows(tmp_path / 'out.tsv') == {4: 'cites-retired', 5: 'cites-retired'}
    assert '2 lines flagged in 1 files: cites-retired 2' in out


LEDGER = """| ID | Kind | Ruling |
|---|---|---|
| A0302-05 | settled | The gull stays on the post. |
| R0302-04-023 | settled | The ford is crossed at the ebb. |
"""

DATED = """# X (outline)

- An old beat, marked 2026-09-01, of the ferry.
- A new beat, marked 2026-11-05, of the ferry.
- A beat settled by A0302-05, the gull on the post.
- A beat settled by R0302-04-023, the ford at the ebb.
- A beat with no mark of any kind at all.
"""


def test_cutoff_flags_older_dates_and_two_part_rulings(tmp_path):
    tree(tmp_path, DATED, LEDGER)
    code, out = run('aged', OUTLINE, '--cutoff', '2026-11-01', '--tsv', 'out.tsv', cwd=tmp_path)
    assert code == 0
    got = rows(tmp_path / 'out.tsv')
    assert got[3] == 'aged'                   # 2026-09-01 < cutoff
    assert 4 not in got                       # 2026-11-05 is newer
    assert got[5] == 'aged'                   # A0302-05 dated 2026-10-26 by the ledger file name
    assert 7 not in got                       # no mark: never aged


def test_no_cutoff_flags_no_age(tmp_path):
    tree(tmp_path, DATED, LEDGER)
    code, out = run('aged', OUTLINE, cwd=tmp_path)
    assert code == 0
    assert '0 lines flagged in 1 files' in out


def test_three_part_ruling_is_dated_by_ledger(tmp_path):
    tree(tmp_path, DATED, LEDGER)
    run('aged', OUTLINE, '--cutoff', '2026-11-01', '--tsv', 'out.tsv', cwd=tmp_path)
    assert rows(tmp_path / 'out.tsv').get(6) == 'aged'


def test_proposals_flags_only_undated(tmp_path):
    tree(tmp_path, """# X (outline)

- *(Proposal.)* The keeper rows out alone at dusk.
- *(Proposal.)* The keeper rows out, 2026-10-02, at dusk.
- *(Proposal.)* The keeper rows out at dusk (A0302-05).
- *(Proposal.)* The keeper rows out at dusk (R0302-04-023).
- The keeper rows out at dusk, not a proposal.
""", LEDGER)
    code, out = run('aged', OUTLINE, '--proposals', '--tsv', 'out.tsv', cwd=tmp_path)
    assert code == 0
    assert rows(tmp_path / 'out.tsv') == {3: 'undated-proposal'}
    assert '1 lines flagged in 1 files: undated-proposal 1' in out
