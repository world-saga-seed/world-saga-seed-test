"""links.py: count broken links (missing files, missing #anchors) in a tree of markdown notes.

The cases plant a link to a file that is not there, an anchor the target has no
heading for, links shown inside `inline code` and fenced code (skipped), web
links (skipped), a repeated heading's numbered anchor, and an --exclude pattern.
"""
import re

from conftest import run, write


def test_smoke_on_the_book(book):
    code, out = run('links', '--root', '.', cwd=book)
    last = out.strip().splitlines()[-1]
    m = re.fullmatch(r'(\d+) broken', last)
    assert m, out
    assert code == (1 if int(m.group(1)) else 0)


def test_smoke_verbose_lists_each_broken_link(book):
    code, out = run('links', '--root', '.', '-v', cwd=book)
    lines = out.strip().splitlines()
    n = int(lines[-1].split()[0])
    listed = [l for l in lines[:-1] if re.match(r'^\S+\.md:\d+  \S', l)]
    assert len(listed) == n


def test_missing_file_is_counted(tmp_path):
    write(tmp_path, {
        'a.md': '# A\n\nSee [the light](b.md) and [the reef](missing.md).\n',
        'b.md': '# B\n',
    })
    code, out = run('links', '--root', '.', '-v', cwd=tmp_path)
    assert code == 1
    assert out.splitlines() == ['a.md:3  missing.md', '1 broken']


def test_existing_file_and_subfolder_link_not_flagged(tmp_path):
    write(tmp_path, {
        'a.md': '# A\n\n[b](sub/b.md)\n',
        'sub/b.md': '# B\n\n[back](../a.md)\n',
    })
    code, out = run('links', '--root', '.', cwd=tmp_path)
    assert (code, out.strip()) == (0, '0 broken')


def test_missing_anchor_is_counted_real_anchor_is_not(tmp_path):
    write(tmp_path, {
        'a.md': '# A\n\n[ok](b.md#the-forty-minutes)\n[bad](b.md#the-fifty-minutes)\n[self](#a)\n[selfbad](#zzz)\n',
        'b.md': '# B\n\n## The Forty Minutes\n\ntext\n',
    })
    code, out = run('links', '--root', '.', '-v', cwd=tmp_path)
    assert code == 1
    assert out.splitlines() == ['a.md:4  b.md#the-fifty-minutes', 'a.md:6  #zzz', '2 broken']


def test_repeated_heading_gets_numbered_anchor(tmp_path):
    write(tmp_path, {
        'a.md': '# A\n\n[one](b.md#notes)\n[two](b.md#notes-1)\n[three](b.md#notes-2)\n',
        'b.md': '# B\n\n## Notes\n\nx\n\n## Notes\n\ny\n',
    })
    code, out = run('links', '--root', '.', '-v', cwd=tmp_path)
    assert out.splitlines() == ['a.md:5  b.md#notes-2', '1 broken']


def test_links_in_inline_code_and_fences_are_skipped(tmp_path):
    write(tmp_path, {
        'a.md': ('# A\n\nWrite a link as `[name](missing.md)` in a card.\n\n'
                 '```\n[name](also-missing.md)\n```\n\n'
                 'A web link [site](https://example.com/x) and [mail](mailto:a@b.c).\n'),
    })
    code, out = run('links', '--root', '.', cwd=tmp_path)
    assert (code, out.strip()) == (0, '0 broken')


def test_link_beside_inline_code_still_checked(tmp_path):
    write(tmp_path, {'a.md': '# A\n\n`[x](fine.md)` but [y](missing.md)\n'})
    code, out = run('links', '--root', '.', '-v', cwd=tmp_path)
    assert (code, out.splitlines()) == (1, ['a.md:3  missing.md', '1 broken'])


def test_exclude_skips_matching_files(tmp_path):
    write(tmp_path, {
        'a.md': '# A\n',
        'existing/old.md': '# Old\n\n[gone](nowhere.md)\n',
    })
    code, out = run('links', '--root', '.', cwd=tmp_path)
    assert (code, out.strip()) == (1, '1 broken')
    code, out = run('links', '--root', '.', '--exclude', 'existing/*', cwd=tmp_path)
    assert (code, out.strip()) == (0, '0 broken')
