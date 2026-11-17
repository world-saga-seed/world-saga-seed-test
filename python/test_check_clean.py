"""check_clean.py: check that a book cloned from the kit has nothing left of the kit's example.

The cases plant: the example book itself (not clean); an example/ folder left
in place; one leftover name in a README; a markdown link into example/; names
inside .git/ (not scanned); near misses (lower case, a longer word, a binary
file) and a clean clone that must print "clean".
"""
from conftest import run, write

CLEAN = {
    'README.md': '# My book\n\nA wren sang on the rookery wall; Rooks and Wrenfield are not names here.\n',
    'story/outline/1-first.md': '# First (outline)\n\n- [the start](../prose/00100-start.md)\n',
    'story/prose/00100-start.md': '# Start\n\nThe ferry came in at noon.\n',
}


def test_smoke_on_book_is_not_clean(book):
    code, out = run('check_clean', '--root', book)
    assert code == 1
    assert 'example name: Wren' in out
    assert out.rstrip().endswith('hits: not clean')


def test_clean_clone(tmp_path):
    write(tmp_path, CLEAN)
    (tmp_path / 'cover.bin').write_bytes(b'\xff\xfe\x00Wren\x80\x81')   # not a text file: skipped
    code, out = run('check_clean', '--root', tmp_path)
    assert code == 0, out
    assert out == 'clean\n'


def test_default_root_is_current_folder(tmp_path):
    write(tmp_path, CLEAN)
    code, out = run('check_clean', cwd=tmp_path)
    assert (code, out) == (0, 'clean\n')


def test_one_leftover_name(tmp_path):
    write(tmp_path, CLEAN)
    write(tmp_path, {'story/notes/00100-start.md': '# Start (notes)\n\nThe ferry from Saltby.\n'})
    code, out = run('check_clean', '--root', tmp_path)
    assert code == 1
    assert out == 'story/notes/00100-start.md:3  example name: Saltby\n1 hits: not clean\n'


def test_example_folder_and_link_into_it(tmp_path):
    write(tmp_path, CLEAN)
    write(tmp_path, {'example/notes.txt': 'nothing named\n',
                     'plan/README.md': '# Plan\n\nSee [the sample](../example/notes.txt) and [web](https://x.org/example/a).\n'})
    code, out = run('check_clean', '--root', tmp_path)
    assert code == 1
    assert 'example/ exists: delete it to start a book' in out
    assert 'plan/README.md:3  link into example/: ../example/notes.txt' in out
    assert 'https' not in out
    assert '2 hits: not clean' in out


def test_git_folder_not_scanned(tmp_path):
    write(tmp_path, CLEAN)
    write(tmp_path, {'.git/COMMIT_EDITMSG': 'Add Wren and Agnes at Skerry Holm\n'})
    code, out = run('check_clean', '--root', tmp_path)
    assert (code, out) == (0, 'clean\n')
