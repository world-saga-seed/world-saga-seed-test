"""knowledge.py: the knowledge-guard entries in force at one chapter, for each narrating head.

The cases plant entries with no span (always in force), a *From* in the future
(left out), an *until* in the past (left out), an *until* at the chapter
(marked as turning), an indented continuation line, an Open section (skipped),
--heads picking one guard, --dir, --out, and a folder with no guards.
"""
from conftest import run, write

TURNS = ' **(turns in this chapter: in force up to the beat where it changes)**'

GUARD = '''# Knowledge guard: Tam

## Knows (true)
- The ferry's hours.
- The bell code. *From* 00300.
  Learned from Dell at the slip.
- The keeper's secret. *From* 00800.

## Believes (wrong, kept on purpose)
1. The tide table is right. *From* 00100 *until* 00500.

## Open
- Whether Tam can swim. *From* 00100.
'''


def entries(out):
    return [l for l in out.splitlines() if l.startswith(('- ', '1. ', '2. '))]


def test_smoke_on_the_book(book):
    counts = {}
    for n in ('00100', '00500', '00600'):
        code, out = run('knowledge', n, cwd=book)
        assert code == 0
        assert out.startswith(f'# Knowledge in force at {n}\n')
        assert '## Knowledge guard: Wren' in out
        counts[n] = len(entries(out))
    assert counts == {'00100': 6, '00500': 8, '00600': 6}
    code, out = run('knowledge', '00500', cwd=book)
    assert sum(TURNS in l for l in out.splitlines()) == 2


def test_spans_in_force_turning_and_open_skipped(tmp_path):
    write(tmp_path, {'story/voice/knowledge/tam.md': GUARD})
    code, out = run('knowledge', '00400', cwd=tmp_path)
    assert entries(out) == [
        "- The ferry's hours.",
        '- The bell code. *From* 00300. Learned from Dell at the slip.',
        '1. The tide table is right. *From* 00100 *until* 00500.',
    ]
    assert '### Knows (true)' in out and '### Believes (wrong, kept on purpose)' in out
    assert 'swim' not in out and '### Open' not in out
    code, out = run('knowledge', '00500', cwd=tmp_path)
    assert f'1. The tide table is right. *From* 00100 *until* 00500.{TURNS}' in out.splitlines()
    code, out = run('knowledge', '00600', cwd=tmp_path)
    assert entries(out) == ["- The ferry's hours.", '- The bell code. *From* 00300. Learned from Dell at the slip.']
    assert '### Believes' not in out          # a section with nothing in force is left out
    code, out = run('knowledge', '00200', cwd=tmp_path)
    assert entries(out) == ["- The ferry's hours.", '1. The tide table is right. *From* 00100 *until* 00500.']
    code, out = run('knowledge', '00800', cwd=tmp_path)
    assert "- The keeper's secret. *From* 00800." in entries(out)


def test_heads_and_dir(tmp_path):
    write(tmp_path, {
        'guards/tam.md': GUARD,
        'guards/wren.md': '# Knowledge guard: Wren\n\n## Knows (true)\n- The lamp.\n',
    })
    code, out = run('knowledge', '00400', '--dir', 'guards', cwd=tmp_path)
    assert '## Knowledge guard: Tam' in out and '## Knowledge guard: Wren' in out
    code, out = run('knowledge', '00400', '--dir', 'guards', '--heads', 'wren', cwd=tmp_path)
    assert '## Knowledge guard: Tam' not in out
    assert entries(out) == ['- The lamp.']


def test_out_writes_the_file(tmp_path):
    write(tmp_path, {'story/voice/knowledge/tam.md': GUARD})
    code, out = run('knowledge', '00400', '--out', 'k.md', cwd=tmp_path)
    assert (code, out) == (0, '')
    text = (tmp_path / 'k.md').read_text()
    assert text.startswith('# Knowledge in force at 00400\n')
    assert '- The bell code. *From* 00300. Learned from Dell at the slip.' in text


def test_no_guard_files_exits_with_message(tmp_path):
    (tmp_path / 'empty').mkdir()
    code, out = run('knowledge', '00400', '--dir', 'empty', cwd=tmp_path)
    assert code == 1
    assert out.strip() == 'no guard files in empty'
    write(tmp_path, {'empty/tam.md': GUARD})
    code, out = run('knowledge', '00400', '--dir', 'empty', '--heads', 'nobody', cwd=tmp_path)
    assert (code, out.strip()) == (1, 'no guard files in empty')
