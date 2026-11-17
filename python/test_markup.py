"""markup.py: the markup page for one chapter, whose beat each passage carries, and the clues, as local HTML.

The cases plant, in a minimal book tree: a ledger row with a three-part ID
(R0302-09-007) of kind settled-author, cited by an outline bullet; a notes
section headed "Reread plants" beside an ordinary one; unmarked and proposal
bullets read with and without --author-written; clue register rows (FP a
herring, a body Kind foreshadowing, a rule Kind a puzzle, one for another
chapter); a linked card; locator finds placed on the page and one not on it.
"""
import json
from conftest import run, write

PROSE = '''# The ford

The tide was out and the ford lay bare under a white sky.

Agnes said the gull on the third post never lied about the water.
'''
OUTLINE = '''# The ford (outline)

## Outline

- Wren crosses the ford at the ebb, as ruled in R0302-09-007, alone.
- The keeper waits on the far side with the lamp unlit and her coat on.
- *(Proposal.)* The gull on the post is the sign she reads, not the table.
- Short bullet.
- The way over is laid stone, see [the causeway](../../world/places/the-causeway.md).
'''
NOTES = '''# The ford (notes)

## Decisions

- The keeper's coat is the old Board coat with brass buttons, worn thin.

## Reread plants

- The gull on the third post comes back when the inspector drowns nearly.
'''
LEDGER = '''| ID | Kind | Ruling |
|---|---|---|
| R0302-09-007 | settled-author | Wren crosses the ford alone at the ebb. |
| R0302-09 | settled | A short ID that must not be read for the long one. |
'''
HOOKS = '''| ID | Clue | Kind | Where |
|---|---|---|---|
| PB-001 | The gull on the third post | body | 00300 |
| FP-002 | The keeper's failing mind | motif | 00300 |
| PB-003 | Forty minutes on every tide | rule | 00300 |
| PB-004 | A clue for another chapter only | body | 00800 |
'''
CARD = '# The causeway: the stone way to the island\n\n*About a mile of laid stone over sand.*\n'


def tree(tmp_path):
    return write(tmp_path, {
        'story/prose/00300-the-ford.md': PROSE,
        'story/outline/00300-the-ford.md': OUTLINE,
        'story/notes/00300-the-ford.md': NOTES,
        'plan/settled/ledger/2027-03-02.md': LEDGER,
        'plan/reread-hooks.md': HOOKS,
        'world/places/the-causeway.md': CARD,
    })


def sources(root, ch='00300'):
    return json.loads((root / 'tmp/markup' / ch / 'sources.json').read_text())


def test_smoke_on_book(book):
    code, out = run('markup', 'items', '00400', cwd=book)
    assert code == 0
    assert out.startswith('tmp/markup/00400/items.md: ')
    assert (book / 'tmp/markup/00400/items.md').read_text().startswith('# Items for 00400')


def test_items_reads_three_part_id_whole(tmp_path):
    tree(tmp_path)
    code, out = run('markup', 'items', '00300', cwd=tmp_path)
    assert code == 0, out
    src = sources(tmp_path)
    assert src['outline:5']['ids'] == ['R0302-09-007']
    assert src['outline:5']['origin'] == 'keyframe'           # its ledger row is settled-author
    assert 'R0302-09-007' in src and src['R0302-09-007']['origin'] == 'keyframe'
    assert 'R0302-09' not in src                              # the short ID is never read out of the long one
    items = (tmp_path / 'tmp/markup/00300/items.md').read_text()
    assert '- R0302-09-007 [decision]: Wren crosses the ford alone at the ebb.' in items


def test_reread_plants_section_is_foreshadow(tmp_path):
    tree(tmp_path)
    run('markup', 'items', '00300', cwd=tmp_path)
    src = sources(tmp_path)
    assert src['notes:9']['head'] == 'Reread plants'
    assert src['notes:9']['layer'] == 'foreshadow'
    assert src['notes:5']['layer'] == 'decision'              # an ordinary notes section
    assert src['outline:6']['layer'] == 'plot'
    assert 'outline:8' not in src                             # under 30 characters: not a source


def test_author_written_makes_unmarked_bullets_keyframes(tmp_path):
    tree(tmp_path)
    run('markup', 'items', '00300', cwd=tmp_path)
    src = sources(tmp_path)
    assert src['outline:6']['origin'] == 'assisted'
    run('markup', 'items', '00300', '--author-written', '00100,00300', cwd=tmp_path)
    src = sources(tmp_path)
    assert src['outline:6']['origin'] == 'keyframe'
    assert src['notes:5']['origin'] == 'keyframe'
    assert src['outline:7']['origin'] == 'assisted'           # a proposal stays assisted


def test_hooks_colours_and_card(tmp_path):
    tree(tmp_path)
    code, out = run('markup', 'items', '00300', cwd=tmp_path)
    items = (tmp_path / 'tmp/markup/00300/items.md').read_text()
    assert '- PB-001 [foreshadow]: The gull on the third post' in items
    assert "- FP-002 [herring]: The keeper's failing mind" in items
    assert '- PB-003 [puzzle]: Forty minutes on every tide' in items
    assert 'PB-004' not in items                              # names another chapter
    assert '- card world/places/the-causeway.md [lore]: The causeway: the stone way to the island. About a mile of laid stone over sand.' in items
    assert '(3 hooks, 1 cards, 1 ledger rows)' in out


def test_render_places_finds_and_drops_the_missing(tmp_path):
    tree(tmp_path)
    run('markup', 'items', '00300', cwd=tmp_path)
    write(tmp_path, {'tmp/markup/00300/finds-a.md':
                     '- outline:5 | plot | the ford lay bare\n'
                     '- PB-001 | foreshadow | the gull on the third post | the sign\n'
                     '- outline:6 | plot | the lamp burned all night\n'
                     '- outline:7 | plot | none\n'})
    code, out = run('markup', 'render', '00300', cwd=tmp_path)
    assert code == 0, out
    assert out.startswith('build/markup/00300.html: 2 finds placed, 1 dropped; ')
    page = (tmp_path / 'build/markup/00300.html').read_text()
    assert '<span class="keyframe" data-tip=' in page and '>the ford lay bare</span>' in page
    assert 'class="assisted foreshadow"' in page
    assert '1 finds not on the page (dropped)' in page
    assert 'the lamp burned all night' in page               # listed as dropped


def test_no_prose_exits(tmp_path):
    tree(tmp_path)
    code, out = run('markup', 'items', '00500', cwd=tmp_path)
    assert code == 1
    assert 'no prose for 00500' in out
