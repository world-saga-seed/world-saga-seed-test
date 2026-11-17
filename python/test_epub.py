"""epub.py: build an EPUB from drafted chapters, so the writer can read a volume as a reader would.

The cases unzip the book and plant: two front pages (one titled by "TITLE=FILE",
one with "[Title]", a "---" and a "- " list); a rights line; a numbered range with
prose, an outline-only slot, an outline-only fragment slot (NNNNN-F1-x.md), a
slot holding the merged mark and a skipped number; two builds with one --uid-seed
and two different titles; --cover with or without Pillow; source line ids, scene
breaks, comments and a "(draft N)" title.
"""
import re, zipfile
import pytest
from conftest import run, write


def unzip(path):
    with zipfile.ZipFile(path) as z:
        return {n: z.read(n) for n in z.namelist()}


def text(files, name):
    return files['OEBPS/' + name].decode('utf-8')


def spine(files):
    return re.findall(r'<itemref idref="([^"]+)"/>', text(files, 'content.opf'))


def tree(tmp_path):
    return write(tmp_path, {
        'prose/00100-the-light.md': '# The light (draft 3)\n\nWren lit the *lamp*.\n\n<!-- a note\nfor me -->\n'
                                    '---\n\n## Later\n\nThe **tide** turned.\n',
        'prose/00200-the-table.md': '# The table\n\nThe table was wrong by forty minutes.\n',
        'outline/00100-the-light.md': '# The light (outline)\n',
        'outline/00300-the-ford.md': '# The ford (outline)\n\n- Wren crosses.\n',
        'outline/00400-old-slot.md': '# Old slot (outline)\n\n**Merged into 00300.**\n',
        'outline/00500-F1-the-gull.md': '# The gull (fragment outline)\n\n- A gull on a post.\n',
        'outline/00600-the-inspector.md': '# The inspector (outline)\n',
        'front/rights.md': '# Copyright\n\nHidden above the rule.\n---\n[Title] is a work of fiction.\n\n- One\n- Two\n\nAfter the list.\n',
        'front/before.md': '# Before you read\n\nA short note.\n',
    })


def build(tmp_path, *args, out='out.epub'):
    code, msg = run('epub', '--title', 'Spring Tides', '--author', 'A. Writer', '--out', out, *args, cwd=tmp_path)
    assert code == 0, msg
    return msg, unzip(tmp_path / out)


RANGE = ('--prose', 'prose', '--outline', 'outline', '--from', '100', '--to', '900')


def test_smoke_on_book(book):
    code, out = run('epub', '--title', 'The Tide Clock: Spring Tides', '--author', 'A. Writer',
                    '--out', 'build/tide-clock.epub', '--prose', 'story/prose', '--outline', 'story/outline',
                    '--from', '100', '--to', '800', cwd=book)
    assert code == 0, out
    assert out.startswith('build/tide-clock.epub: 2 pages, about ')
    files = unzip(book / 'build/tide-clock.epub')
    assert files['mimetype'] == b'application/epub+zip'
    assert spine(files) == ['titlepage', 'c00400', 'c00700']
    assert '<title>Caught on the causeway</title>' in text(files, 'c00700.xhtml')


def test_two_front_pages_in_order_with_title_list_and_series(tmp_path):
    tree(tmp_path)
    msg, files = build(tmp_path, '--series', 'The Tide Clock', '--front', 'Rights page=front/rights.md',
                       '--front', 'front/before.md', 'prose/00200-the-table.md')
    assert spine(files) == ['titlepage', 'front', 'front2', 'c-00200-the-table']
    rights = text(files, 'front.xhtml')
    assert '<title>Rights page</title>' in rights            # TITLE=FILE sets the page title
    assert 'Hidden above the rule' not in rights             # only what follows "---"
    assert '<p>The Tide Clock, Spring Tides is a work of fiction.</p>' in rights
    assert '<ul>\n<li>One</li>\n<li>Two</li>\n</ul>\n<p>After the list.</p>' in rights
    assert '<title>Before you read</title>' in text(files, 'front2.xhtml')
    assert '<p>A short note.</p>' in text(files, 'front2.xhtml')
    opf = text(files, 'content.opf')
    assert '<meta name="calibre:series" content="The Tide Clock"/>' in opf


def test_title_without_series_and_no_rights(tmp_path):
    tree(tmp_path)
    msg, files = build(tmp_path, '--front', 'front/rights.md', 'prose/00200-the-table.md')
    assert '<p>Spring Tides is a work of fiction.</p>' in text(files, 'front.xhtml')
    assert '<title>Copyright</title>' in text(files, 'front.xhtml')
    assert '<dc:rights>' not in text(files, 'content.opf')


def test_rights_in_content_opf(tmp_path):
    tree(tmp_path)
    msg, files = build(tmp_path, '--rights', 'All rights reserved & kept', 'prose/00200-the-table.md')
    assert '<dc:rights>All rights reserved &amp; kept</dc:rights>' in text(files, 'content.opf')


def test_range_skip_merged_and_fragment(tmp_path):
    tree(tmp_path)
    msg, files = build(tmp_path, *RANGE, '--skip', '600', '--merged-mark', '**Merged into')
    assert spine(files) == ['titlepage', 'c00100', 'c00200', 'c00300', 'c00500']
    assert 'c00400.xhtml' not in str(list(files))            # the merged slot
    assert 'OEBPS/c00600.xhtml' not in files                 # skipped
    assert '<p class="placeholder">[Not yet drafted.]</p>' in text(files, 'c00300.xhtml')
    assert '<title>The ford</title>' in text(files, 'c00300.xhtml')
    frag = text(files, 'c00500.xhtml')
    assert '<title>Fragment: The gull</title>' in frag
    assert '<body class="fragment">' in frag
    msg, files = build(tmp_path, *RANGE)                     # without the options both slots come back
    assert spine(files) == ['titlepage', 'c00100', 'c00200', 'c00300', 'c00400', 'c00500', 'c00600']


def test_chapter_text_line_ids_and_title(tmp_path):
    tree(tmp_path)
    msg, files = build(tmp_path, 'prose/00100-the-light.md')
    page = text(files, 'c-00100-the-light.xhtml')
    assert '<title>The light</title>' in page                # "(draft 3)" dropped
    assert '<p id="p3">Wren lit the <em>lamp</em>.</p>' in page
    assert 'a note' not in page and 'for me' not in page
    assert '<p id="p7" class="break">*</p>' in page
    assert '<h3 id="p9">Later</h3>' in page
    assert '<p id="p11">The <strong>tide</strong> turned.</p>' in page


def test_uid_seed_gives_same_identifier(tmp_path):
    tree(tmp_path)
    uid = re.compile(r'<dc:identifier id="uid">([^<]+)</dc:identifier>')
    _, a = build(tmp_path, '--uid-seed', 'tide-clock-1', 'prose/00200-the-table.md', out='a.epub')
    code, msg = run('epub', '--title', 'Another Title', '--out', 'b.epub', '--uid-seed', 'tide-clock-1',
                    'prose/00200-the-table.md', cwd=tmp_path)
    b = unzip(tmp_path / 'b.epub')
    assert uid.search(text(a, 'content.opf')).group(1) == uid.search(text(b, 'content.opf')).group(1)
    code, msg = run('epub', '--title', 'Another Title', '--out', 'c.epub', 'prose/00200-the-table.md', cwd=tmp_path)
    c = unzip(tmp_path / 'c.epub')
    assert uid.search(text(c, 'content.opf')).group(1) != uid.search(text(a, 'content.opf')).group(1)


def test_cover(tmp_path):
    tree(tmp_path)
    try:
        import PIL  # noqa: F401  (the tool runs under the same interpreter)
        have = True
    except ImportError:
        have = False
    msg, files = build(tmp_path, '--cover', 'prose/00200-the-table.md')
    if have:
        assert files['OEBPS/cover.jpg'][:2] == b'\xff\xd8'
        assert 'OEBPS/title.xhtml' not in files
        assert spine(files)[0] == 'cover'
        assert '<meta name="cover" content="cover-image"/>' in text(files, 'content.opf')
    else:
        assert 'Pillow not found; built with a title page, no cover' in msg
        assert 'OEBPS/title.xhtml' in files and 'OEBPS/cover.jpg' not in files


def test_no_cover_keeps_title_page(tmp_path):
    tree(tmp_path)
    msg, files = build(tmp_path, 'prose/00200-the-table.md')
    assert 'OEBPS/cover.jpg' not in files
    assert '<h1>Spring Tides</h1>' in text(files, 'title.xhtml')
    assert '<p class="byline">A. Writer</p>' in text(files, 'title.xhtml')


def test_needs_chapters(tmp_path):
    code, out = run('epub', '--title', 'X', '--out', 'x.epub', cwd=tmp_path)
    assert code == 2
    assert 'give chapter files, or --prose with --from and --to' in out
