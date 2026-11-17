"""firstuse.py: setting words a chapter is the first to use that three or more cards also use.

The cases plant a possessive ("board's", "boards'") that must fold to the word
with no trailing apostrophe, a plural folded to its singular, a word earlier
chapters already used (not repeated), --batch K reporting only the last K
files, --min-cards, --cards pointing at another folder, and words under
"## Notes" (--stop).
"""
import pytest

from conftest import run, write

CARDS = {
    'world/a.md': '# A: one\n\nThe board sent a winch and a pawl.\n',
    'world/b.md': '# B: two\n\nThe board kept the winch, the pawl and the lamp.\n',
    'world/sub/c.md': '# C: three\n\nThe board paid for the winch and the lamp.\n',
}


def entries(out):
    return [l for l in out.splitlines() if l.startswith('- **')]


def test_smoke_on_the_book(book):
    code, out = run('firstuse', 'story/prose/00400-the-forty-minutes.md', '--cards', 'world', cwd=book)
    assert code == 0
    assert out.startswith('## 00400-the-forty-minutes.md\n')
    assert '- **almanac** (4 cards), line 3: …' in out


def test_possessive_folds_to_the_word(tmp_path):
    write(tmp_path, CARDS)
    write(tmp_path, {'01.md': "The board's man came by.\n", '02.md': "All the boards' rules held.\n"})
    code, out = run('firstuse', '01.md', cwd=tmp_path)
    assert [e.split(', line')[0] for e in entries(out)] == ['- **board** (3 cards)']
    assert "board'" not in out.replace("board's man", '')
    code, out = run('firstuse', '02.md', cwd=tmp_path)
    assert [e.split(', line')[0] for e in entries(out)] == ['- **board** (3 cards)']
    assert "**board'" not in out and "**boards" not in out


def test_plural_folds_and_line_shown(tmp_path):
    write(tmp_path, CARDS)
    write(tmp_path, {'01.md': '# Chapter one\n\nShe oiled the boards before dawn.\n'})
    code, out = run('firstuse', '01.md', cwd=tmp_path)
    assert out.splitlines()[0] == '## 01.md'
    assert entries(out) == ['- **board** (3 cards), line 3: …She oiled the boards before dawn.…']


def test_es_plural_folds_to_singular(tmp_path):
    write(tmp_path, CARDS)
    write(tmp_path, {'01.md': 'She oiled the winches before dawn.\n'})
    code, out = run('firstuse', '01.md', cwd=tmp_path)
    assert [e.split(', line')[0] for e in entries(out)] == ['- **winch** (3 cards)']


def test_word_seen_earlier_is_not_new_and_batch_reports_last_k(tmp_path):
    write(tmp_path, CARDS)
    write(tmp_path, {
        '01.md': 'The winch turned.\n',
        '02.md': 'Nothing of note.\n',
        '03.md': 'The winch and the board.\n',
    })
    code, out = run('firstuse', '01.md', '02.md', '03.md', '--batch', '1', cwd=tmp_path)
    assert '## 01.md' not in out and '## 02.md' not in out
    assert out.splitlines()[0] == '## 03.md'
    assert [e.split(' (')[0] for e in entries(out)] == ['- **board**']    # winch is set up by 01
    code, out = run('firstuse', '01.md', '02.md', '03.md', cwd=tmp_path)
    assert [l for l in out.splitlines() if l.startswith('## ')] == ['## 01.md', '## 03.md']
    code, out = run('firstuse', '01.md', '02.md', '03.md', '--batch', '2', cwd=tmp_path)
    assert [l for l in out.splitlines() if l.startswith('## ')] == ['## 03.md']


def test_min_cards(tmp_path):
    write(tmp_path, CARDS)
    write(tmp_path, {'01.md': 'A pawl slipped and the lamp went out.\n'})
    code, out = run('firstuse', '01.md', cwd=tmp_path)
    assert out.strip() == ''                         # pawl in 2 cards, lamp in 2
    code, out = run('firstuse', '01.md', '--min-cards', '2', cwd=tmp_path)
    assert [e.split(', line')[0] for e in entries(out)] == ['- **pawl** (2 cards)', '- **lamp** (2 cards)']


def test_cards_dir_and_stop(tmp_path):
    write(tmp_path, {f'lore/{k[6:]}': v for k, v in CARDS.items()})
    write(tmp_path, {'01.md': 'Nothing here.\n\n## Notes\n\nThe winch.\n'})
    code, out = run('firstuse', '01.md', cwd=tmp_path)             # default world/ is absent
    assert out.strip() == ''
    code, out = run('firstuse', '01.md', '--cards', 'lore', '--stop', '^## Never', cwd=tmp_path)
    assert [e.split(', line')[0] for e in entries(out)] == ['- **winch** (3 cards)']
    code, out = run('firstuse', '01.md', '--cards', 'lore', cwd=tmp_path)
    assert out.strip() == ''
