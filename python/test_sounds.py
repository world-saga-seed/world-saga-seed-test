"""sounds.py: sound spans on the page (phonetic letters between slashes), held to the book's convention.

The cases plant: one span used twice in one chapter (both uses count no earlier
chapter) and again in the next (one earlier chapter); a span in speech beside one
in narration; a forbidden symbol; a slash pair with no phonetic letter (not a
span) and the --chars that makes it one; a --stop heading; --batch and --volume
with the rarity flag on one chapter and off on two.
"""
from conftest import run, write

CH1 = '''# One

"Say /ˈtʃɑk/," she said.
He tried it: "/ˈtʃɑk/."

And/or the gate was open, a/b test.
'''
CH2 = '''# Two

"/ˈtʃɑk/," said the keeper.
The word came back to me as /ˈtʃɑk/ in my head.
'''
CH3 = '''# Three

Nothing sounded strange that day.
'''


def tree(tmp_path):
    return write(tmp_path, {'c1.md': CH1, 'c2.md': CH2, 'c3.md': CH3})


def test_smoke_on_book(book):
    code, out = run('sounds', 'story/prose/00400-the-forty-minutes.md', cwd=book)
    assert code == 0
    assert out.startswith('# Sound spans\n')
    assert 'Spans in the volume:' in out


def test_repeat_in_one_chapter_counts_no_earlier_chapter(tmp_path):
    tree(tmp_path)
    code, out = run('sounds', 'c1.md', 'c2.md', cwd=tmp_path)
    assert code == 0
    assert '- c1:3 /ˈtʃɑk/ in speech; earlier chapters: 0' in out
    assert '- c1:4 /ˈtʃɑk/ in speech; earlier chapters: 0' in out   # same chapter, second use
    assert '- c2:3 /ˈtʃɑk/ in speech; earlier chapters: 1' in out
    assert '- c2:4 /ˈtʃɑk/ **in narration**; earlier chapters: 1' in out
    assert 'a/b' not in out and 'And/or' not in out                  # no phonetic letter: not a span
    assert 'Spans in the volume: in 2 chapter(s).' in out
    assert 'Rare' not in out


def test_forbid_flags_a_forbidden_symbol(tmp_path):
    write(tmp_path, {'c1.md': '# One\n\n"/ˈwɔːtə/," she said, and "/ˈtʃɑk/."\n'})
    code, out = run('sounds', 'c1.md', '--forbid', 'ː ɹ', cwd=tmp_path)
    assert code == 0
    assert '- c1:3 /ˈwɔːtə/ in speech; earlier chapters: 0; **forbidden: ː**' in out
    assert '- c1:3 /ˈtʃɑk/ in speech; earlier chapters: 0\n' in out   # near miss: nothing forbidden


def test_batch_reports_only_the_last_files(tmp_path):
    tree(tmp_path)
    code, out = run('sounds', 'c1.md', 'c2.md', '--batch', '1', cwd=tmp_path)
    assert '- c1:' not in out
    assert '- c2:3 /ˈtʃɑk/ in speech; earlier chapters: 1' in out


def test_volume_with_one_span_chapter_is_rare(tmp_path):
    tree(tmp_path)
    code, out = run('sounds', 'c1.md', 'c2.md', 'c3.md', '--batch', '1', '--volume', '2', cwd=tmp_path)
    assert code == 0
    assert 'None.' in out                    # the batch (c3) has no span
    assert ('Spans in the volume: in 1 chapter(s). **Rare: check each span reads as a sound, not a slip.**') in out
    code, out = run('sounds', 'c1.md', 'c2.md', 'c3.md', '--volume', '3', cwd=tmp_path)
    assert 'Spans in the volume: in 2 chapter(s).' in out and 'Rare' not in out


def test_chars_and_stop(tmp_path):
    write(tmp_path, {'c1.md': '# One\n\n"/kat/," she said.\n\n## Notes\n\n"/ˈtʃɑk/" in the notes.\n'})
    code, out = run('sounds', 'c1.md', cwd=tmp_path)
    assert 'None.' in out                    # /kat/ has no IPA letter; the notes are not read
    assert 'Spans in the volume: in 0 chapter(s).' in out
    code, out = run('sounds', 'c1.md', '--chars', 'k', cwd=tmp_path)
    assert '- c1:3 /kat/ in speech; earlier chapters: 0' in out
    code, out = run('sounds', 'c1.md', '--stop', '^## Nothing', cwd=tmp_path)
    assert '- c1:7 /ˈtʃɑk/ in speech; earlier chapters: 0' in out
