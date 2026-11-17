"""tells.py: texture numbers for chapters (similes, negations, sentence lengths, knots) and a banned-word scan.

The cases plant "the way anybody" and "the way anyone" similes beside "the way
home" (not a simile), a --count pattern with a known rate per 10,000 words, a
35-word sentence with a semicolon (a knot) beside a long one without, banned
words in narration and in dialogue, and a banned word kept under "## Notes".
"""
import re

from conftest import run, write


def field(out, name, key):
    line = next(l for l in out.splitlines() if l.startswith(name))
    return re.search(re.escape(key) + r'=\s*([\d.]+)', line).group(1)


def test_smoke_on_the_book(book):
    code, out = run('tells', 'story/prose/00400-the-forty-minutes.md', 'story/voice/samples/sample-pages.md',
                    '--banned', 'story/voice/banned.txt', cwd=book)
    assert code == 0
    lines = out.splitlines()
    assert lines[0].startswith('00400-the-forty-minutes.md ')
    assert ' w=' in lines[0] and ' button%=' in lines[0]
    assert any(l.startswith('sample-pages.md ') for l in lines)
    assert re.search(r'^\d+ banned-word hits', out, re.M)


def test_way_anybody_and_way_anyone_count_as_the_simile(tmp_path):
    write(tmp_path, {
        'a.md': 'She stood the way anybody would. He ran the way anyone would.\n',
        'b.md': 'She knew the way home. He lost the way north.\n',
    })
    code, out = run('tells', 'a.md', 'b.md', cwd=tmp_path)
    assert code == 0
    assert field(out, 'a.md', 'way/k') == '166.7'    # 2 in 12 words
    assert field(out, 'b.md', 'way/k') == '0.0'


def test_simile_in_dialogue_not_counted(tmp_path):
    write(tmp_path, {'a.md': '"Do it the way anyone would," she said to me.\n'})
    code, out = run('tells', 'a.md', cwd=tmp_path)
    assert field(out, 'a.md', 'way/k') == '0.0'
    assert field(out, 'a.md', 'w') == '4'


def test_count_prints_rate_per_ten_thousand(tmp_path):
    write(tmp_path, {'a.md': 'The Tide came and the tide went. ' + ' '.join(['stone'] * 33) + '.\n'})  # 40 words
    code, out = run('tells', 'a.md', '--count', r'tide=\btide\b', '--count', r'gull=\bgull\b', cwd=tmp_path)
    line = out.splitlines()[0]
    assert ' w=   40 ' in line
    assert line.endswith(' tide/10k=500.0 gull/10k= 0.0')


def test_knot_line_for_long_sentence_with_semicolon(tmp_path):
    long_semi = ('The water came over the third post before the bell had rung for the evening '
                 'and the keeper stood at the rail with the glass held up to her eye; she said '
                 'nothing to me about the hour at all')
    long_plain = long_semi.replace(';', ',')
    short_semi = 'The lamp was lit; the door was shut'
    write(tmp_path, {'a.md': long_semi + '.\n', 'b.md': long_plain + '.\n\n' + short_semi + '.\n'})
    n = len(long_semi.split())
    assert n >= 35
    code, out = run('tells', 'a.md', 'b.md', cwd=tmp_path)
    knots = [l for l in out.splitlines() if 'knot' in l]
    assert knots == [f'    knot ({n} words): {long_semi[:160]}']   # the line shows the first 160 characters


def test_banned_words_narration_only_unless_all_text(tmp_path):
    write(tmp_path, {
        'banned.txt': '# words the narrator never uses\ntapestry\nre:\\bdelv(e|ed|ing)\\b\n',
        'a.md': ('# Title with tapestry\n\nA tapestry hung by the door.\n\n'
                 '"No tapestry here," she said.\n\nWe delved into the chest.\n\n## Notes\n\ntapestry again\n'),
    })
    code, out = run('tells', 'a.md', '--banned', 'banned.txt', cwd=tmp_path)
    assert out.split('\n\n', 1)[1].strip().splitlines() == [
        '2 banned-word hits:',
        'a.md:3  tapestry  | A tapestry hung by the door.',
        'a.md:7  delved  | We delved into the chest.',
    ]
    code, out = run('tells', 'a.md', '--banned', 'banned.txt', '--all-text', cwd=tmp_path)
    assert '3 banned-word hits:' in out
    assert 'a.md:5  tapestry  | "No tapestry here," she said.' in out
    code, out = run('tells', 'a.md', '--banned', 'banned.txt', '--stop', '^## Never', cwd=tmp_path)
    assert 'a.md:11  tapestry  | tapestry again' in out


def test_no_banned_list_prints_no_hit_line(tmp_path):
    write(tmp_path, {'a.md': 'A plain line.\n'})
    code, out = run('tells', 'a.md', cwd=tmp_path)
    assert code == 0
    assert 'banned-word hits' not in out
