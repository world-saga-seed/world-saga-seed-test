"""refrains.py: a watch list of refrains counted per chapter, and six-word runs shared by three chapters or more.

The cases plant a refrain over the volume and chapter limits, one under them,
a sentence repeated in three files (listed as one joined run) and in two (not),
a repeated run made mostly of small words (skipped), --batch K deciding whether
a run reaches the batch, and a refrain kept under "## Notes" (--stop).
"""
from conftest import run, write

DOG = 'The old dog lay down by the cold hearth.'


def near(out):
    return out.split('## Near-verbatim', 1)[1].strip().splitlines()[2:]


def test_smoke_on_the_book(book):
    write(book, {'refrains.txt': '# watch list\nand forty\t\\band forty\\b\n'})
    code, out = run('refrains', 'story/voice/samples/sample-pages.md', 'story/prose/00400-the-forty-minutes.md',
                    '--list', 'refrains.txt', cwd=book)
    assert code == 0
    assert out.startswith('# Refrains, sample-pages to 00400-the-forty-minutes\n')
    assert '| Refrain | Volume | Per chapter | Flag |' in out
    assert '## Near-verbatim in three chapters or more (a six-word run shared)' in out


def test_watch_list_counted_and_flagged(tmp_path):
    write(tmp_path, {
        'list.txt': '# refrains\ntorn ear\t\\btorn ear\\b\ncough\t\\bcough(ed)?\\b\nunused\t\\bzebra\\b\n',
        '01-a.md': 'The dog had a torn ear.\n',
        '02-b.md': 'Torn ear. A torn ear. The torn ear twitched. His torn ear. He coughed.\n',
        '03-c.md': 'The torn ear again.\n\n## Notes\n\ntorn ear torn ear torn ear\n',
    })
    code, out = run('refrains', '01-a.md', '02-b.md', '03-c.md', '--list', 'list.txt', '--volume-max', '5', cwd=tmp_path)
    rows = out.split('|---|---|---|---|\n', 1)[1].split('\n\n', 1)[0].splitlines()
    assert rows == [
        '| torn ear | 6 | 01-a 1, 02-b 4, 03-c 1 | over 5 in the volume; 02-b: 4 |',
        '| cough | 1 | 02-b 1 |  |',
    ]
    code, out = run('refrains', '01-a.md', '02-b.md', '03-c.md', '--list', 'list.txt', '--chapter-max', '4', cwd=tmp_path)
    assert '| torn ear | 6 | 01-a 1, 02-b 4, 03-c 1 |  |' in out
    code, out = run('refrains', '01-a.md', '02-b.md', '03-c.md', '--list', 'list.txt',
                    '--stop', '^## Never', '--volume-max', '20', cwd=tmp_path)
    assert '| torn ear | 9 | 01-a 1, 02-b 4, 03-c 4 | 02-b: 4; 03-c: 4 |' in out


def test_six_word_run_in_three_files_listed(tmp_path):
    write(tmp_path, {
        'list.txt': 'x\t\\bzebra\\b\n',
        '01-a.md': f'Morning came. {DOG} Wren swept.\n',
        '02-b.md': f'Rain all day. {DOG} Agnes read.\n',
        '03-c.md': f'Night fell. {DOG} Nobody spoke.\n',
    })
    code, out = run('refrains', '01-a.md', '02-b.md', '03-c.md', '--list', 'list.txt', cwd=tmp_path)
    assert near(out) == ['- "the old dog lay down by the cold hearth": 01-a, 02-b, 03-c']


def test_run_in_two_files_not_listed(tmp_path):
    write(tmp_path, {
        'list.txt': 'x\t\\bzebra\\b\n',
        '01-a.md': f'{DOG}\n',
        '02-b.md': f'{DOG}\n',
        '03-c.md': 'Something else entirely happened on the island that night.\n',
    })
    code, out = run('refrains', '01-a.md', '02-b.md', '03-c.md', '--list', 'list.txt', cwd=tmp_path)
    assert near(out) == ['None.']


def test_run_of_small_words_skipped(tmp_path):
    s = 'It was in the back of the house by noon.'
    write(tmp_path, {'list.txt': 'x\t\\bzebra\\b\n', '01-a.md': s + '\n', '02-b.md': s + '\n', '03-c.md': s + '\n'})
    code, out = run('refrains', '01-a.md', '02-b.md', '03-c.md', '--list', 'list.txt', cwd=tmp_path)
    assert near(out) == ['None.']


def test_list_with_batch_reports_only_runs_reaching_the_batch(tmp_path):
    write(tmp_path, {
        'list.txt': 'dog\t\\bdog\\b\n',
        '01-a.md': f'{DOG}\n',
        '02-b.md': f'{DOG}\n',
        '03-c.md': f'{DOG}\n',
        '04-d.md': 'The gulls were loud over the rocks all that grey morning.\n',
    })
    files = ['01-a.md', '02-b.md', '03-c.md', '04-d.md']
    code, out = run('refrains', *files, '--list', 'list.txt', '--batch', '1', cwd=tmp_path)
    assert code == 0
    assert '| dog | 3 | 01-a 1, 02-b 1, 03-c 1 |  |' in out     # the count still covers the volume
    assert near(out) == ['None.']
    code, out = run('refrains', *files, '--list', 'list.txt', '--batch', '2', cwd=tmp_path)
    assert near(out) == ['- "the old dog lay down by the cold hearth": 01-a, 02-b, 03-c']
