"""repeats.py: phrases of 5 to 8 words found in N or more files, and stock patterns counted per file.

The cases plant a phrase in three files (listed) and one in two (not, at the
default of 3), a phrase only in dialogue (gone with --narration), a --tics file
of label<TAB>regex patterns counted per file, a file whose title matches
--skip-title, and --min-n/--max-n bounds.
"""
from conftest import run, write

SHARED = 'the salt wind came over the dunes'


def three(tmp_path):
    return write(tmp_path, {
        'a.md': f'# A\n\nAt noon {SHARED} toward us. The bell rang.\n',
        'b.md': f'# B\n\nBy night {SHARED} again. The gull cried out once and was gone.\n',
        'c.md': f'# C\n\nIn March {SHARED} hard. The gull cried out once and was gone.\n',
    })


def phrases(out):
    rows = out.split('## Phrases in', 1)[1].strip().splitlines()[4:]
    return rows


def test_smoke_on_the_book(book):
    code, out = run('repeats', 'story/voice/samples/sample-pages.md', 'story/prose/00400-the-forty-minutes.md',
                    '--min-files', '2', cwd=book)
    assert code == 0
    assert out.startswith('# Repeats\n')
    assert '| Pattern | sample-pages | 00400-the-fo | All |' in out
    assert '## Phrases in 2 or more files' in out


def test_phrase_in_three_files_listed_two_files_not(tmp_path):
    three(tmp_path)
    code, out = run('repeats', 'a.md', 'b.md', 'c.md', cwd=tmp_path)
    assert phrases(out) == [f'| {SHARED} | 3 | a, b, c |']
    code, out = run('repeats', 'a.md', 'b.md', 'c.md', '--min-files', '2', cwd=tmp_path)
    assert phrases(out) == [f'| {SHARED} | 3 | a, b, c |',
                            '| the gull cried out once and was gone | 2 | b, c |']


def test_no_phrase_prints_none_row(tmp_path):
    write(tmp_path, {'a.md': 'One thing here.\n', 'b.md': 'Another thing there.\n'})
    code, out = run('repeats', 'a.md', 'b.md', '--min-files', '2', cwd=tmp_path)
    assert phrases(out) == ['| (none) | 0 | |']


def test_narration_drops_quoted_phrase(tmp_path):
    write(tmp_path, {
        'a.md': '"Mind the clock on the landing wall," she said.\n',
        'b.md': '"Mind the clock on the landing wall," he said.\n',
    })
    code, out = run('repeats', 'a.md', 'b.md', '--min-files', '2', cwd=tmp_path)
    assert '| mind the clock on the landing wall | 2 | a, b |' in out
    code, out = run('repeats', 'a.md', 'b.md', '--min-files', '2', '--narration', cwd=tmp_path)
    assert out.startswith('# Repeats (narration only)\n')
    assert phrases(out) == ['| (none) | 0 | |']


def test_tics_file_counts_per_file_and_replaces_builtins(tmp_path):
    write(tmp_path, {
        'tics.tsv': '# my narrator\nbell\t\\bbells?\\b\nno tab line is skipped\nsighed\t\\bsighed\\b\n',
        'a.md': 'The bell rang. Two bells rang. She sighed.\n',
        'b.md': 'A bell. A belly laugh.\n',
    })
    code, out = run('repeats', 'a.md', 'b.md', '--tics', 'tics.tsv', cwd=tmp_path)
    table = out.split('## Patterns per file', 1)[1].split('## Phrases', 1)[0].strip().splitlines()
    assert table == ['| Pattern | a | b | All |', '|---|---|---|---|',
                     '| bell | 2 | 1 | 3 |', '| sighed | 1 | 0 | 1 |']


def test_builtin_tics_without_file(tmp_path):
    write(tmp_path, {'a.md': 'He stood as if asleep, as though dead. For a moment, nothing.\n'})
    code, out = run('repeats', 'a.md', cwd=tmp_path)
    assert '| "as if / as though" | 2 | 2 |' in out
    assert '| "for a moment" / "a long moment" | 1 | 1 |' in out


def test_skip_title_leaves_file_out(tmp_path):
    three(tmp_path)
    write(tmp_path, {'c.md': f'# Interlude: the keeper\n\nIn March {SHARED} hard.\n'})
    code, out = run('repeats', 'a.md', 'b.md', 'c.md', '--skip-title', '^# Interlude', cwd=tmp_path)
    assert '| Pattern | a | b | All |' in out
    assert phrases(out) == ['| (none) | 0 | |']
    code, out = run('repeats', 'a.md', 'b.md', 'c.md', '--skip-title', '^# Prologue', cwd=tmp_path)
    assert f'| {SHARED} | 3 | a, b, c |' in out


def test_min_n_max_n_bound_the_phrase_length(tmp_path):
    write(tmp_path, {'a.md': 'X the copper kettle boiled dry Y.\n', 'b.md': 'Z the copper kettle boiled dry W.\n'})
    code, out = run('repeats', 'a.md', 'b.md', '--min-files', '2', cwd=tmp_path)
    assert '| the copper kettle boiled dry | 2 | a, b |' in out
    code, out = run('repeats', 'a.md', 'b.md', '--min-files', '2', '--min-n', '6', cwd=tmp_path)
    assert phrases(out) == ['| (none) | 0 | |']
    code, out = run('repeats', 'a.md', 'b.md', '--min-files', '2', '--min-n', '3', '--max-n', '3', cwd=tmp_path)
    assert '| copper kettle boiled | 2 | a, b |' in out
    assert 'the copper kettle boiled dry' not in out
