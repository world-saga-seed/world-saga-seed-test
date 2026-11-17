"""quotes.py: check that every quote in a report is really in the text it quotes.

The cases plant a quote that resolves and one that does not, a report with no
quotes (exit 1, "0 quotes found"), curly quotes and *emphasis* in the text
against straight quotes in the report, a --section that checks only its own
lines (and its subheadings), --backticks spans, -v, and several --in files.
"""
from conftest import run, write

TEXT = ('“Forty,” she said, and   *the lamp* was lit.\n\n'
        'The water came over the third post at a quarter past nine.\n')


def test_smoke_on_the_book(book):
    code, out = run('quotes', 'reports/critic-facts-00400.md', '--in', 'reports/snapshot/00400-the-forty-minutes.md', cwd=book)
    assert code == 1
    assert 'MISSING  reports/critic-facts-00400.md:' in out
    assert 'the lens was cleaned every Sunday' in out
    assert out.strip().splitlines()[-1] == '2 of 3 quotes resolve'
    code, out = run('quotes', 'reports/keep-00400.md', '--in', 'story/prose/00400-the-forty-minutes.md', cwd=book)
    assert (code, out.strip()) == (0, '6 of 6 quotes resolve')


def test_missing_quote_reported_with_line(tmp_path):
    write(tmp_path, {
        'text.md': TEXT,
        'report.md': ('# Findings\n\n- quote: the third post at a quarter past nine\n'
                      '- quote: the fourth post at ten\n'),
    })
    code, out = run('quotes', 'report.md', '--in', 'text.md', cwd=tmp_path)
    assert code == 1
    assert out.splitlines() == ['MISSING  report.md:4  the fourth post at ten', '1 of 2 quotes resolve']


def test_no_quotes_exits_1(tmp_path):
    write(tmp_path, {'text.md': TEXT, 'report.md': '# Findings\n\nNothing found; the chapter is clean.\n'})
    code, out = run('quotes', 'report.md', '--in', 'text.md', cwd=tmp_path)
    assert (code, out.strip()) == (1, '0 quotes found')


def test_curly_quotes_emphasis_and_spacing_still_match(tmp_path):
    write(tmp_path, {
        'text.md': TEXT,
        'report.md': ('- quote: "Forty," she said, and the lamp was lit\n'
                      '* **quote**: "the lamp was lit"\n'
                      'quote: “Forty,” she said\n'),
    })
    code, out = run('quotes', 'report.md', '--in', 'text.md', '-v', cwd=tmp_path)
    assert code == 0, out
    assert out.splitlines()[-1] == '3 of 3 quotes resolve'
    assert sum(l.startswith('ok       report.md:') for l in out.splitlines()) == 3


def test_section_checks_only_that_section(tmp_path):
    write(tmp_path, {
        'text.md': TEXT,
        'report.md': ('# Report\n\n## Findings\n\n- quote: words that are not there\n\n'
                      '## Next pass\n\n- quote: the lamp was lit\n\n### Detail\n\n- quote: the third post\n\n'
                      '## Dropped\n\n- quote: other words not there\n'),
    })
    code, out = run('quotes', 'report.md', '--in', 'text.md', cwd=tmp_path)
    assert (code, out.splitlines()[-1]) == (1, '2 of 4 quotes resolve')
    code, out = run('quotes', 'report.md', '--in', 'text.md', '--section', '## Next pass', cwd=tmp_path)
    assert (code, out.strip()) == (0, '2 of 2 quotes resolve')
    code, out = run('quotes', 'report.md', '--in', 'text.md', '--section', '## Dropped', cwd=tmp_path)
    assert code == 1
    assert out.splitlines() == ['MISSING  report.md:17  other words not there', '0 of 1 quotes resolve']


def test_backticks_checked_only_with_flag(tmp_path):
    write(tmp_path, {
        'text.md': TEXT,
        'report.md': '- `the third post` and `a post never written`\n- quote: the lamp was lit\n',
    })
    code, out = run('quotes', 'report.md', '--in', 'text.md', cwd=tmp_path)
    assert (code, out.strip()) == (0, '1 of 1 quotes resolve')
    code, out = run('quotes', 'report.md', '--in', 'text.md', '--backticks', cwd=tmp_path)
    assert code == 1
    assert out.splitlines() == ['MISSING  report.md:1  a post never written', '2 of 3 quotes resolve']


def test_several_in_files(tmp_path):
    write(tmp_path, {
        'one.md': 'The bell rang at noon.\n',
        'two.md': 'The gull cried once.\n',
        'report.md': '- quote: The bell rang at noon.\n- quote: The gull cried once.\n',
    })
    code, out = run('quotes', 'report.md', '--in', 'one.md', cwd=tmp_path)
    assert out.strip().splitlines()[-1] == '1 of 2 quotes resolve'
    code, out = run('quotes', 'report.md', '--in', 'one.md', 'two.md', cwd=tmp_path)
    assert (code, out.strip()) == (0, '2 of 2 quotes resolve')
