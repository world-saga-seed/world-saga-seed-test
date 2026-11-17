"""gaps.py: trace each critic finding to the drafter's bundle, and list the fixes to the source."""
from conftest import run, write

CARD = ('# Selkie: a beast\n\n*Summary.*\n\nKeywords: seal\n\n## Selkie\n\n'
        '- **Body.** Grey.\n- **Size.** Two arms long.\n- **Threat.** Bites.\n')
MAN = ('# what the drafter of 00500 was given\n# commit abc1234\n'
       'world/beast/selkie.md\tfields: Body\n'
       'world/things/the-log.md\tcited: not given\n'
       'story/outline/00500-the-inspector.md\tthe chapter, inline\n')


def finding(n, quote, against, sev='break'):
    return f'{n}. **Finding**\n- quote: {quote}\n- against: {against}\n- why: x\n- severity: {sev}\n- direction: y\n'


def book(tmp_path, report):
    return write(tmp_path, {
        'world/beast/selkie.md': CARD,
        'world/things/the-log.md': '# The Log: a book\n\n*S.*\n\nKeywords: ledger\n\n- **What it is.** A book.\n',
        'world/things/the-oar.md': '# The Oar: an oar\n\n*S.*\n\nKeywords: oar\n',
        'story/outline/00500-the-inspector.md': '# 00500\n',
        'story/prose/00400-earlier.md': '# 00400\n\nThe boat was red.\n',
        'story/voice/voice.md': '# Voice\n',
        'man.tsv': MAN, 'crit/report.md': '# Critic\n\n' + report})


def trace(tmp_path, *extra):
    return run('gaps', 'crit/report.md', '--manifest', 'man.tsv', '--rules', 'story/voice/voice.md',
               '--chapter', '00500', *extra, cwd=tmp_path)


def test_each_kind_of_source(tmp_path):
    book(tmp_path, '\n'.join([
        finding(1, 'grey', '"Grey." world/beast/selkie.md, Body'),
        finding(2, 'long', '"Two arms long." world/beast/selkie.md, Size'),
        finding(3, 'book', 'world/things/the-log.md, What it is'),
        finding(4, 'oar', 'world/things/the-oar.md'),
        finding(5, 'red', 'story/prose/00400-earlier.md:3'),
        finding(6, 'voice', 'story/voice/voice.md, the rule'),
        finding(7, 'beat', 'the outline, beat 2'),
        finding(8, 'nothing', 'common sense'),
        finding(9, 'gone', 'world/things/no-such.md'),
        finding(10, 'taste', 'world/beast/selkie.md', sev='taste')]))
    code, out = trace(tmp_path)
    assert code == 0
    row = {l.split('|')[2].strip(): l for l in out.split('\n') if l.startswith('| report.md') or '/report.md' in l}
    assert 'given' in row['1'] and 'not given' not in row['1']
    assert 'field not given: Size' in row['2']
    assert 'not included' in row['3'] and 'not included' in row['4']
    assert 'earlier page' in row['5'] and 'not read' in row['5']
    assert '| rules' in row['6'] and '| chapter' in row['7'] and 'no source' in row['8']
    assert 'no such file' in row['9'] and '10' not in row               # taste is not traced by default
    fixes = out.split('## Fixes to the source', 1)[1]
    assert 'include `world/beast/selkie.md` with Size' in fixes
    assert 'include `world/things/the-log.md`' in fixes and 'include `world/things/the-oar.md`' in fixes
    assert 'card the page fact from `story/prose/00400-earlier.md` (findings 5)' in fixes


def test_a_short_name_resolves_to_the_one_file(tmp_path):
    book(tmp_path, finding(1, 'long', 'selkie.md, Size'))
    code, out = trace(tmp_path)
    assert '`world/beast/selkie.md`' in out and 'field not given: Size' in out


def test_the_chapter_own_draft_is_not_a_source(tmp_path):
    book(tmp_path, finding(1, 'x', 'story/prose/00500-the-inspector.md:4 and world/beast/selkie.md, Body'))
    write(tmp_path, {'story/prose/00500-the-inspector.md': '# 00500\n'})
    code, out = trace(tmp_path)
    assert '00500-the-inspector' not in out.split('## Fixes')[0].split('\n', 2)[2]
    assert 'None: every traced finding' in out


def test_severity_option(tmp_path):
    book(tmp_path, finding(1, 'taste', 'world/beast/selkie.md, Size', sev='taste'))
    code, out = trace(tmp_path, '--severity', 'taste')
    assert 'field not given: Size' in out
