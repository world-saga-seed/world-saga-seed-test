"""reading.py: one chapter's reading list, one hop from its outline and notes.

The cases plant a linked card (listed whole), a link with an #anchor into a
large file (listed by that section's line range), a card named only by a
keyword and one by a person's first name (both found without a link), a card
nobody names (left out), a character sheet named by first name, the chapter
before in prose (a later chapter is not), a link to another outline (listed as
not to read), --step narrowing the list, --digest, --large, and a chapter with
no outline (exits with a message).
"""
from conftest import run, write


def card(name, what, kw, body='Text.'):
    return f'# {name}: {what}\n\n*Summary.*\n\nKeywords: {kw}\n\n{body}\n'


BIG = ('# The Light: the lamp room\n\n*Summary.*\n\nKeywords: lamp\n\n'
       '## Wicks\n\nTrim them square and short each dusk.\n\n'
       '## Oil\n\nColza oil, kept warm in winter.\n')


def small_book(tmp_path):
    return write(tmp_path, {
        'story/outline/00500-the-inspector.md': (
            '# 00500 The inspector\n\n'
            '- Agnes and Wren at [the light](../../world/things/the-light.md#oil).\n'
            '- The [log](../../world/things/the-log.md) is written up.\n'
            '- Out past the reef the boats wait.\n'
            '- See [the arc](1-arc.md).\n'),
        'story/outline/1-arc.md': '# The arc\n',
        'story/notes/00500-the-inspector.md': '# Notes\n\n- Dell rows the inspector over.\n',
        'world/things/the-light.md': BIG,
        'world/things/the-log.md': card('The Log', 'the keeper\'s book', 'ledger'),
        'world/places/bell-rock.md': card('Bell Rock', 'a skerry', 'reef, breakers'),
        'world/people/dell-harker.md': card('Dell Harker', 'the ferryman', 'boatman'),
        'world/people/mary-quill.md': card('Mary Quill', 'the post woman', 'letters'),
        'world/README.md': '# World\n',
        'story/notes/characters/wren.md': '# Wren Ashby: the narrator\n\n## At a glance\n\nThirteen.\n\n## Habits\n\nCounts steps.\nHums.\n',
        'story/notes/characters/tom.md': '# Tom Pike: a boy\n',
        'story/prose/00400-the-forty-minutes.md': '# 00400\n\nProse.\n',
        'story/prose/00300-earlier.md': '# 00300\n\nProse.\n',
        'story/prose/00600-later.md': '# 00600\n\nProse.\n',
        'story/voice/voice.md': '# Voice\n',
        'story/volume/1-digest.md': '# Digest\n',
    })


def section(out, title):
    return out.split(f'## {title}\n', 1)[1].split('\n## ', 1)[0].strip().splitlines()


def test_smoke_on_the_book(book):
    code, out = run('reading', '00400', cwd=book)
    assert code == 0
    assert out.startswith('# Reading list for 00400 (drafter)\n')
    assert '- `story/outline/00400-the-forty-minutes.md` (whole)' in out
    assert '`story/outline/1-spring-tides.md`' in section(out, 'Linked but not to read')
    assert any(l.startswith('- `story/notes/characters/wren.md`') for l in section(out, 'People'))


def test_drafter_list(tmp_path):
    small_book(tmp_path)
    code, out = run('reading', '00500', '--large', '20', cwd=tmp_path)
    assert code == 0
    assert section(out, 'Rules') == ['- `story/voice/voice.md`', '- two or three of `story/voice/samples/`']
    assert section(out, 'The chapter') == ['- `story/outline/00500-the-inspector.md` (whole)',
                                           '- `story/notes/00500-the-inspector.md` (whole)']
    cards = section(out, 'Cards and sections')
    assert cards[0].startswith('- `world/people/dell-harker.md` (whole, ')        # by first name
    assert cards[1].startswith('- `world/places/bell-rock.md` (whole, ')          # by keyword "reef"
    assert cards[2].startswith('- `world/things/the-light.md` (')                 # by link, one section
    assert cards[2].endswith(' words in all; read only these sections, by line):')
    assert cards[3].startswith('  - lines 11 to 14: "Oil" (8 words)')
    assert cards[4].startswith('- `world/things/the-log.md` (whole, ')
    assert len(cards) == 5
    assert 'mary-quill' not in out and 'README' not in out
    assert section(out, 'Linked but not to read')[-1] == '`story/outline/1-arc.md`'
    people = section(out, 'People')
    assert len(people) == 1 and people[0].startswith('- `story/notes/characters/wren.md` (whole, ')
    assert section(out, 'Prose') == ['- `story/prose/00400-the-forty-minutes.md`: the chapter before; read closely']


def test_large_default_lists_small_file_whole(tmp_path):
    small_book(tmp_path)
    code, out = run('reading', '00500', cwd=tmp_path)
    assert any(l.startswith('- `world/things/the-light.md` (whole, ') for l in section(out, 'Cards and sections'))
    assert 'lines 11 to 14' not in out


def test_digest(tmp_path):
    small_book(tmp_path)
    code, out = run('reading', '00500', '--digest', 'story/volume/1-digest.md', cwd=tmp_path)
    assert section(out, 'Prose')[0] == ("- `story/volume/1-digest.md`: what the volume's pages have already set; "
                                        'read whole, in place of the earlier chapters')


def test_step_habits_lists_only_the_habits_section(tmp_path):
    small_book(tmp_path)
    code, out = run('reading', '00500', '--step', 'habits', cwd=tmp_path)
    assert out.startswith('# Reading list for 00500 (habits)\n')
    assert '## Rules' not in out and '## Cards and sections' not in out and '## Prose' not in out
    people = section(out, 'People')
    assert people[0].startswith('- `story/notes/characters/wren.md` (')
    assert people[1].startswith('  - lines 7 to 11: "Habits" (5 words)')


def test_step_continuity_lists_only_prose(tmp_path):
    small_book(tmp_path)
    code, out = run('reading', '00500', '--step', 'continuity', cwd=tmp_path)
    heads = [l for l in out.splitlines() if l.startswith('## ')]
    assert heads == ['## The chapter', '## Prose']


def test_no_outline_exits_with_message(tmp_path):
    small_book(tmp_path)
    code, out = run('reading', '00900', cwd=tmp_path)
    assert (code, out.strip()) == (1, 'no outline or notes for 00900')
