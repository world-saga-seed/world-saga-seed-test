"""scale.py: the scale sheet for a chapter, the viewpoint's height and every size phrase.

The cases plant: a heights file whose second range holds the chapter; a chapter
past every range (no height, the phrases still listed); a facts file with a
comment, in place of the default adult line; two --other heights either side of
the viewpoint; a reference word ("belt") used in a size phrase in a neighbouring
chapter; a chapter with no size phrase; a chapter with no prose file.
"""
from conftest import run, write

ADULT = 'an adult man is about 170 cm: belt at about 100, a counter or bench top 90 to 100'


def tree(tmp_path):
    return write(tmp_path, {
        'story/prose/00300-a.md': '# A\n\nThe counter came up to my chest. She was taller than the door.\n',
        'story/prose/00400-b.md': '# B\n\nThe rail was level with his belt, cold.\n\nNothing here measures anything.\n',
        'story/prose/00500-c.md': '# C\n\nThe wind dropped and the boats came in.\n',
        'story/prose/00900-d.md': '# D\n\nHis coat reached my belt when he stood.\n',
        'heights.txt': '00100 00399 140\n00400 00699 150  # a growth year\n',
    })


def test_smoke_on_book(book):
    code, out = run('scale', '00400', '--height', '152', cwd=book)
    assert code == 0
    assert '# Scale sheet, 00400' in out
    assert '- **Viewpoint:** about 152 cm.' in out
    assert '## Size phrases on the page' in out


def test_heights_file_picks_the_range_holding_the_chapter(tmp_path):
    tree(tmp_path)
    code, out = run('scale', '00400', '--heights', 'heights.txt', cwd=tmp_path)
    assert code == 0
    assert '- **Viewpoint:** about 150 cm.' in out
    assert ('- **On the viewpoint\'s body:** eyes 140, chin 130, shoulder 123, chest 108, '
            'waist 90, hip 75, knee 42 cm.') in out
    code, out = run('scale', '00300', '--heights', 'heights.txt', cwd=tmp_path)
    assert '- **Viewpoint:** about 140 cm.' in out


def test_chapter_past_every_range_has_no_height_but_lists_phrases(tmp_path):
    tree(tmp_path)
    code, out = run('scale', '00900', '--heights', 'heights.txt', cwd=tmp_path)
    assert code == 0
    assert '- **Viewpoint:** no height for 00900; add a line to heights.txt.' in out
    assert "On the viewpoint's body" not in out
    assert '- 00900:3 "His coat reached my belt when he stood."' in out


def test_facts_file_replaces_the_adult_line(tmp_path):
    tree(tmp_path)
    write(tmp_path, {'facts.txt': '# the setting\ncounters are built at 80 cm\n\nthe fisher folk stand about 160\n'})
    code, out = run('scale', '00400', '--height', '150', '--facts', 'facts.txt', cwd=tmp_path)
    assert code == 0
    assert '- **A hand** is about 9 cm; counters are built at 80 cm; the fisher folk stand about 160.' in out
    assert ADULT not in out
    code, out = run('scale', '00400', '--height', '150', cwd=tmp_path)
    assert f'- **A hand** is about 9 cm; {ADULT}.' in out


def test_other_prints_hands_taller_and_shorter(tmp_path):
    tree(tmp_path)
    code, out = run('scale', '00400', '--height', '150', '--other', 'Agnes=168', '--other', 'Tam=141', cwd=tmp_path)
    assert code == 0
    assert '- **Agnes:** 168 cm, 2.0 hands taller.' in out
    assert '- **Tam:** 141 cm, 1.0 hands shorter.' in out


def test_size_phrases_and_repeat_near(tmp_path):
    tree(tmp_path)
    code, out = run('scale', '00300', '--height', '140', cwd=tmp_path)
    assert '- 00300:3 "The counter came up to my chest."' in out
    assert '- 00300:3 "She was taller than the door."' in out
    assert 'repeat near' not in out          # no watch word in either phrase
    code, out = run('scale', '00400', '--height', '150', cwd=tmp_path)
    assert '- 00400:3 "The rail was level with his belt, cold."  **repeat near:** 00900:3 (belt)' in out
    assert 'Nothing here' not in out
    code, out = run('scale', '00500', '--height', '150', cwd=tmp_path)
    assert out.rstrip().endswith('## Size phrases on the page\n\n- none')


def test_no_prose_file_prints_sheet_only(tmp_path):
    tree(tmp_path)
    code, out = run('scale', '00700', '--height', '150', cwd=tmp_path)
    assert code == 0
    assert '- **Viewpoint:** about 150 cm.' in out
    assert '## Size phrases' not in out


def test_needs_a_height(tmp_path):
    tree(tmp_path)
    code, out = run('scale', '00400', cwd=tmp_path)
    assert code == 2
    assert 'give --height or --heights' in out
