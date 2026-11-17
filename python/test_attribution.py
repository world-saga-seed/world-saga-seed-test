"""attribution.py: unlabeled paragraphs for a blind attribution test, and the key to score it.

The cases plant: two heads in one file split by line ranges, and a second file
with one head throughout; six long paragraphs per head and one short one (under
--min-words) that is never picked; a paragraph after "## Notes" (cut by --stop);
--count, --seed (the same test rebuilt), and a key that names each P's file,
line and head.
"""
import re
from conftest import run, write

WORDS = ' '.join(['word'] * 45)


def para(tag):
    return f'{tag} {WORDS}.'


def tree(tmp_path):
    # a.md: lines 1-12 Ada (six long paragraphs, one short), 13-24 Ben (six long).
    a = []
    for k in range(6):
        a += [para(f'Ada{k}'), '']
    b = []
    for k in range(6):
        b += [para(f'Ben{k}'), '']
    a_text = '\n'.join(a[:11] + ['Ada short line of few words.'] + b[:11] + ['']) + '\n'
    c_text = '# Cal\n\n' + '\n\n'.join(para(f'Cal{k}') for k in range(3)) + '\n\n## Notes\n\n' + para('CalNote') + '\n'
    return write(tmp_path, {'a.md': a_text, 'c.md': c_text})


HEADS = 'a.md:1-12=Ada,a.md:13-24=Ben,c.md=Cal'


def test_smoke_on_book(book):
    code, out = run('attribution', 'story/prose/00400-the-forty-minutes.md',
                    '--heads', '00400-the-forty-minutes.md=Wren', '--out', 'test.md', '--key', 'key.md',
                    '--min-words', '10', cwd=book)
    assert code == 0, out
    assert re.match(r'\d+ paragraphs: Wren \d+', out)
    assert (book / 'test.md').read_text().startswith('# Unlabeled paragraphs\n\n## P1\n')
    assert ', Wren' in (book / 'key.md').read_text()


def test_count_with_five_from_each_head(tmp_path):
    tree(tmp_path)
    code, out = run('attribution', 'a.md', 'c.md', '--heads', HEADS, '--out', 'test.md', '--key', 'key.md',
                    '--count', '13', cwd=tmp_path)
    assert code == 0, out
    assert '13 paragraphs: Ada 5, Ben 5, Cal 3' in out


def test_short_paragraph_and_notes_never_picked(tmp_path):
    tree(tmp_path)
    code, out = run('attribution', 'a.md', 'c.md', '--heads', HEADS, '--out', 'test.md', '--key', 'key.md',
                    '--count', '50', cwd=tmp_path)
    assert '15 paragraphs: Ada 6, Ben 6, Cal 3' in out
    t = (tmp_path / 'test.md').read_text()
    assert 'short line' not in t
    assert 'CalNote' not in t
    code, out = run('attribution', 'a.md', 'c.md', '--heads', HEADS, '--out', 'test.md', '--key', 'key.md',
                    '--count', '50', '--stop', '^## Nothing', cwd=tmp_path)
    assert 'Cal 4' in out                    # the notes paragraph read once --stop no longer matches
    code, out = run('attribution', 'a.md', 'c.md', '--heads', HEADS, '--out', 'test.md', '--key', 'key.md',
                    '--count', '50', '--min-words', '3', cwd=tmp_path)
    assert 'Ada 7' in out                    # the short paragraph counts under a lower --min-words


def test_key_names_file_line_and_head(tmp_path):
    tree(tmp_path)
    run('attribution', 'a.md', 'c.md', '--heads', HEADS, '--out', 'test.md', '--key', 'key.md', '--count', '50',
        cwd=tmp_path)
    test = (tmp_path / 'test.md').read_text()
    key = (tmp_path / 'key.md').read_text().splitlines()
    assert key[0] == '# Attribution key'
    entries = dict(re.match(r'- (P\d+): (.+)', k).groups() for k in key[2:])
    assert len(entries) == 15
    for p, where in entries.items():
        para_text = test.split(f'## {p}\n\n', 1)[1].split('\n', 1)[0]
        tag = para_text.split()[0]
        head = tag.rstrip('0123456789')
        f, rest = where.split(':')
        line, h = rest.split(', ')
        assert h == head
        src = (tmp_path / f).read_text().split('\n')[int(line) - 1]
        assert src == para_text


def test_seed_rebuilds_the_same_test(tmp_path):
    tree(tmp_path)
    for out in ('t1.md', 't2.md'):
        run('attribution', 'a.md', 'c.md', '--heads', HEADS, '--out', out, '--key', 'k.md', '--seed', '3',
            cwd=tmp_path)
    run('attribution', 'a.md', 'c.md', '--heads', HEADS, '--out', 't3.md', '--key', 'k.md', '--seed', '4',
        cwd=tmp_path)
    t1, t2, t3 = ((tmp_path / f).read_text() for f in ('t1.md', 't2.md', 't3.md'))
    assert t1 == t2
    assert t1 != t3
