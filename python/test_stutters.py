"""stutters.py: the same short phrase twice within a few paragraphs of one chapter, and capped frames.

The cases plant a three-word content run 80 words apart (a hit) and 300 apart
(not, at the default --window 250), a run used six times (a standing phrase,
not a hit), an all-filler three-word run (not a hit) and an all-filler
four-word run inside 100 words (a hit), --clues and --notes files marking a
hit "clue?" (only notes whose names start with the chapter's number count),
"as if" over its cap and twice in a paragraph, and --summary.
"""
import itertools
import re

from conftest import run, write

PHRASE = 'copper kettle boiled'


def filler(n, start=0):
    """n distinct nonsense words, so they make no repeated runs of their own."""
    letters = 'bcdfghjklmnpqrstvwxz'
    words = (''.join(t) for t in itertools.product(letters, 'aeiou', letters))
    return ' '.join(itertools.islice(words, start, start + n))


def chapter(gap, uses=2):
    """PHRASE used `uses` times, `gap` filler words between uses, one paragraph each."""
    paras = []
    k = 0
    for u in range(uses):
        paras.append(f'{PHRASE} {filler(gap, k)}' if u < uses - 1 else PHRASE + ' ' + filler(5, k))
        k += gap
    return '\n\n'.join(paras) + '\n'


def test_smoke_on_the_book(book):
    code, out = run('stutters', 'story/prose/00400-the-forty-minutes.md', cwd=book)
    assert code == 0
    assert out.startswith('# Stutters, window 250 words, 1 files\n')
    assert '## 00400-the-forty-minutes.md: ' in out
    assert out.strip().splitlines()[-1].startswith('**Total:** ')


def test_run_80_words_apart_is_a_hit(tmp_path):
    write(tmp_path, {'00400-x.md': chapter(80)})
    code, out = run('stutters', '00400-x.md', cwd=tmp_path)
    assert '## 00400-x.md: 1 hits' in out
    assert f'| 1, 3 | 83 | {PHRASE} |' in out.splitlines()
    assert out.strip().endswith('**Total:** 1 hits.')


def test_run_300_words_apart_is_not_a_hit_unless_window_widened(tmp_path):
    write(tmp_path, {'00400-x.md': chapter(300)})
    code, out = run('stutters', '00400-x.md', cwd=tmp_path)
    assert '## 00400-x.md: 0 hits' in out
    assert PHRASE not in out
    code, out = run('stutters', '00400-x.md', '--window', '400', cwd=tmp_path)
    assert out.startswith('# Stutters, window 400 words, 1 files\n')
    assert f'| 1, 3 | 303 | {PHRASE} |' in out.splitlines()


def test_run_used_six_times_is_standing_not_a_hit(tmp_path):
    write(tmp_path, {'00400-x.md': chapter(20, uses=6)})
    code, out = run('stutters', '00400-x.md', cwd=tmp_path)
    assert '## 00400-x.md: 0 hits' in out
    assert f'- Standing phrases (not hits): {PHRASE}' in out
    write(tmp_path, {'00400-y.md': chapter(20, uses=5)})
    code, out = run('stutters', '00400-y.md', cwd=tmp_path)
    hits = int(re.search(r'## 00400-y.md: (\d+) hits', out).group(1))
    assert hits >= 4                                # five uses: at least each later use is a hit
    assert f'| 1, 3 | 23 | {PHRASE} |' in out.splitlines()
    assert 'Standing phrases' not in out
    code, out = run('stutters', '00400-y.md', '--standing', '5', cwd=tmp_path)
    assert f'- Standing phrases (not hits): {PHRASE}' in out


def test_filler_runs(tmp_path):
    write(tmp_path, {
        'a.md': f'it was the {filler(80)}\n\nit was the {filler(5, 80)}\n',
        'b.md': f'as if he were {filler(50)}\n\nas if he were {filler(5, 50)}\n',
        'c.md': f'as if he were {filler(150)}\n\nas if he were {filler(5, 150)}\n',
    })
    code, out = run('stutters', 'a.md', 'b.md', 'c.md', cwd=tmp_path)
    assert '## a.md: 0 hits' in out                 # three filler words: not a hit
    assert '## b.md: 1 hits' in out and '| 1, 3 | 54 | as if he were |' in out
    assert '## c.md: 0 hits' in out                 # all filler past 100 words


def test_clues_file_marks_hit(tmp_path):
    write(tmp_path, {
        '00400-x.md': chapter(80),
        'hooks.md': '- The copper kettle boiled dry the night the inspector came.\n',
        'other.md': '- A kettle on the hob.\n',
    })
    code, out = run('stutters', '00400-x.md', '--clues', 'hooks.md', cwd=tmp_path)
    assert f'| 1, 3 | 83 | {PHRASE} **clue?** |' in out
    code, out = run('stutters', '00400-x.md', '--clues', 'other.md', cwd=tmp_path)
    assert f'| 1, 3 | 83 | {PHRASE} |' in out.splitlines()
    code, out = run('stutters', '00400-x.md', '--clues', 'other.md', '--clues', 'hooks.md', cwd=tmp_path)
    assert '**clue?**' in out


def test_notes_dir_uses_only_the_chapters_own_notes(tmp_path):
    write(tmp_path, {
        'prose/00400-x.md': chapter(80),
        'prose/00500-y.md': chapter(80),
        'notes/00400-x.md': '- Plant: the copper kettle boiled.\n',
        'notes/00500-y.md': '- Nothing here.\n',
        'notes/1-arc.md': '- the copper kettle boiled (arc note)\n',
    })
    code, out = run('stutters', 'prose/00400-x.md', 'prose/00500-y.md', '--notes', 'notes', cwd=tmp_path)
    x, y = out.split('## 00500-y.md', 1)
    assert f'| 1, 3 | 83 | {PHRASE} **clue?** |' in x
    assert f'| 1, 3 | 83 | {PHRASE} |' in y.splitlines()


def test_as_if_over_cap_and_twice_in_a_paragraph(tmp_path):
    write(tmp_path, {'a.md': (f'as if {filler(10)} as though {filler(10, 10)}\n\n'
                              f'as if {filler(10, 20)}\n\nas if {filler(10, 30)}\n\nas if {filler(10, 40)}\n')})
    code, out = run('stutters', 'a.md', cwd=tmp_path)
    assert '- **Over cap:** "as if" / "as though" 5 (cap 4)' in out
    assert '- **Twice in a paragraph:** "as if" / "as though" x2 at line 1' in out
    write(tmp_path, {'b.md': f'as if {filler(10)}\n\nas if {filler(10, 10)}\n'})
    code, out = run('stutters', 'b.md', cwd=tmp_path)
    assert 'Over cap' not in out and 'Twice in a paragraph' not in out


def test_summary_one_line_per_chapter(tmp_path):
    write(tmp_path, {'00400-x.md': chapter(80), '00500-y.md': chapter(300)})
    code, out = run('stutters', '00400-x.md', '00500-y.md', '--summary', cwd=tmp_path)
    lines = out.strip().splitlines()
    assert '| 00400-x.md | 1 | 0 |  |' in lines
    assert '| 00500-y.md | 0 | 0 |  |' in lines
    assert PHRASE not in out
    assert lines[-1] == '**Total:** 1 hits.'


def test_stop_heading(tmp_path):
    write(tmp_path, {'a.md': f'{PHRASE} {filler(20)}\n\n## Notes\n\n{PHRASE} again\n'})
    code, out = run('stutters', 'a.md', cwd=tmp_path)
    assert '## a.md: 0 hits' in out
    code, out = run('stutters', 'a.md', '--stop', '## Never', cwd=tmp_path)
    assert '## a.md: 1 hits' in out
