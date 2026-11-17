"""check_leak.py: check that a change meant for the kit carries nothing of your book.

The cases plant, in a unified diff read from a file or standard input: a name
from a card heading and from a character sheet (the longer name reported, not
its parts); a run of eight words shared with the book's prose, and a shorter run
caught only under --words; an email address (a noreply@ one not flagged); and a
clean change with lower-case and removed-line near misses that must print "clean".
"""
from conftest import run, write

BOOK = {
    'world/people/agnes-rook.md': '# Agnes Rook: the keeper of the light\n\nBody.\n',
    'world/places/saltby.md': '# Saltby: the harbor village\n\nBody.\n',
    'world/README.md': '# Zebedee World\n\nAn index, not a card.\n',
    'story/notes/characters/wren.md': '# Wren Ashby (character sheet)\n',
    'story/prose/00100-x.md': '# X\n\nThe water on the holm runs forty minutes behind the printed table.\n',
}


def diff(*added, removed=('',)):
    lines = ['--- a/tools/critic.md', '+++ b/tools/critic.md', '@@ -1,3 +10,4 @@', ' context line']
    lines += ['-' + r for r in removed if r]
    lines += ['+' + a for a in added]
    return '\n'.join(lines) + '\n'


def leak(tmp_path, text, *args):
    write(tmp_path / 'book', BOOK)
    write(tmp_path, {'change.diff': text})
    return run('check_leak', '--book', 'book', '--diff', 'change.diff', *args, cwd=tmp_path)


def test_smoke_on_book(book):
    d = diff('Read the chapter as Wren would read it.')
    code, out = run('check_leak', '--book', book, stdin=d)
    assert code == 1
    assert 'tools/critic.md:11  name "Wren"' in out


def test_clean_change(tmp_path):
    d = diff('A wren and a rook are birds; saltby is lower case.', 'Keep the voice sheet short.',
             removed=('Agnes Rook was here.',))
    code, out = leak(tmp_path, d)
    assert (code, out) == (0, 'clean\n')


def test_names_from_cards_and_sheets(tmp_path):
    d = diff('Ask Agnes Rook about it.', 'Then Saltby, then Ashby.', 'The Zebedee index.')
    code, out = leak(tmp_path, d)
    assert code == 1
    assert out == ('tools/critic.md:11  name "Agnes Rook"\n'
                   'tools/critic.md:12  name "Saltby"\n'
                   'tools/critic.md:12  name "Ashby"\n'
                   '3 hits: read each before offering the change\n')


def test_shared_run_and_words(tmp_path):
    d = diff('Note that the water on the holm runs forty minutes behind schedule.',
             'It runs forty minutes behind, they say.')
    code, out = leak(tmp_path, d)
    assert code == 1
    assert 'tools/critic.md:11  shared run "the water on the holm runs forty minutes"' in out
    assert 'critic.md:12' not in out          # five shared words, under the default eight
    assert '1 hits' in out
    code, out = leak(tmp_path, d, '--words', '4')
    assert 'tools/critic.md:12  shared run "runs forty minutes behind"' in out


def test_email_but_not_noreply(tmp_path):
    d = diff('Write to me at jo.writer@example.com for it.', 'Co-Authored-By: Bot <noreply@anthropic.com>')
    code, out = leak(tmp_path, d)
    assert code == 1
    assert out == 'tools/critic.md:11  email jo.writer@example.com\n1 hits: read each before offering the change\n'
