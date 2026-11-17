"""cards.py: check card heads and folder tables, build the tables and the subject index, find cards.

The cases plant a card head out of form, a stale table, a README with no
markers and one whose marker comment is worded differently, a name carrying a
"(proposal)" status mark, a loose file at the top of the root, keywords the
card's text already uses, and words found in a head or only in the text. One
case copies the tool to another folder and checks the index header names it.
"""
import shutil

from conftest import KIT, run, write

MARK = '<!-- cards: built by tools/cards.py; do not edit -->'


def card(name, what, summary='A short line.', kw='rocks, shoal', body='More text.'):
    return f'# {name}: {what}\n\n*{summary}*\n\nKeywords: {kw}\n\n{body}\n'


def world(tmp_path, readme_begin=MARK, extra=None):
    files = {
        'world/places/README.md': f'# Places\n\n{readme_begin}\n<!-- /cards -->\n',
        'world/places/bell-rock.md': card('Bell Rock', 'a reef off the holm', kw='skerry, breakers'),
        'world/places/the-causeway.md': card('The Causeway', 'the stone road to Saltby', kw='tide road, posts'),
    }
    files.update(extra or {})
    return write(tmp_path, files)


TABLE = ('| Card | What it is |\n|---|---|\n'
         '| [Bell Rock](bell-rock.md) | a reef off the holm |\n'
         '| [The Causeway](the-causeway.md) | the stone road to Saltby |')


def test_smoke_check_on_the_book(book):
    code, out = run('cards', 'check', '--root', 'world', cwd=book)
    assert (code, out.strip().splitlines()[-1]) == (0, '0 card problems')


def test_build_writes_the_table_then_check_passes(tmp_path):
    world(tmp_path)
    code, out = run('cards', 'check', '--root', 'world', cwd=tmp_path)
    assert code == 1
    assert out.splitlines() == ['world/places/README.md: table is stale; run build', '1 card problems']
    code, out = run('cards', 'build', '--root', 'world', cwd=tmp_path)
    assert (code, out.strip()) == (0, 'rebuilt world/places')
    text = (tmp_path / 'world/places/README.md').read_text()
    assert text == f'# Places\n\n{MARK}\n{TABLE}\n<!-- /cards -->\n'
    code, out = run('cards', 'check', '--root', 'world', cwd=tmp_path)
    assert (code, out.strip()) == (0, '0 card problems')


def test_head_out_of_form_is_reported(tmp_path):
    world(tmp_path, extra={'world/places/bad.md': '# Bad Card: a thing\n\n*Summary.*\n\nTags: none\n'})
    run('cards', 'build', '--root', 'world', cwd=tmp_path)
    code, out = run('cards', 'check', '--root', 'world', cwd=tmp_path)
    assert code == 1
    assert out.splitlines() == ['world/places/bad.md: line 5 is not "Keywords: ..."', '1 card problems']


def test_marker_worded_differently_is_found(tmp_path):
    world(tmp_path, readme_begin='<!-- cards: anything -->')
    code, out = run('cards', 'build', '--root', 'world', cwd=tmp_path)
    assert out.strip() == 'rebuilt world/places'
    text = (tmp_path / 'world/places/README.md').read_text()
    assert text == f'# Places\n\n<!-- cards: anything -->\n{TABLE}\n<!-- /cards -->\n'
    code, out = run('cards', 'check', '--root', 'world', cwd=tmp_path)
    assert (code, out.strip()) == (0, '0 card problems')


def test_readme_without_markers_is_reported(tmp_path):
    world(tmp_path, readme_begin='<!-- table here -->')
    code, out = run('cards', 'build', '--root', 'world', cwd=tmp_path)
    assert out.strip() == 'world/places/README.md: no table markers, skipped'
    code, out = run('cards', 'check', '--root', 'world', cwd=tmp_path)
    assert code == 1
    assert 'world/places/README.md: no table markers' in out.splitlines()


def test_mark_proposal_dropped_from_table_and_index(tmp_path):
    world(tmp_path, extra={'world/places/gull-stack.md': card('Gull Stack (proposal)', 'a sea stack', kw='nesting cliff')})
    run('cards', 'build', '--root', 'world', cwd=tmp_path)
    text = (tmp_path / 'world/places/README.md').read_text()
    assert '| [Gull Stack (proposal)](gull-stack.md) | a sea stack |' in text   # no --mark: the name keeps it
    run('cards', 'build', '--index', '--root', 'world', '--mark', 'proposal', cwd=tmp_path)
    text = (tmp_path / 'world/places/README.md').read_text()
    assert '| [Gull Stack](gull-stack.md) | a sea stack |' in text
    assert '(proposal)' not in text
    index = (tmp_path / 'world/INDEX.md').read_text()
    assert '- **Gull Stack**: [Gull Stack: a sea stack](places/gull-stack.md)' in index
    assert '(proposal)' not in index


def test_build_index_writes_index_and_lists_loose_file(tmp_path):
    world(tmp_path, extra={'world/glossary.md': '# Glossary: words of the coast\n\nholm: an island.\n'})
    code, out = run('cards', 'build', '--index', '--root', 'world', cwd=tmp_path)
    assert code == 0
    assert out.splitlines()[-1].startswith('world/INDEX.md: ')
    assert out.splitlines()[-1].endswith(' entries')
    index = (tmp_path / 'world/INDEX.md').read_text()
    assert index.startswith('# Subject index\n')
    assert '- **Glossary**: [Glossary: words of the coast](glossary.md)' in index
    assert '- **Bell Rock**: [Bell Rock: a reef off the holm](places/bell-rock.md)' in index
    assert '- **Skerry**: [Bell Rock: a reef off the holm](places/bell-rock.md)' in index
    assert '- **Places**: [Places](places/README.md)' in index
    assert 'INDEX' not in index.split('\n', 1)[1]   # the index does not list itself


def test_index_header_names_the_path_the_tool_ran_from(tmp_path):
    world(tmp_path)
    (tmp_path / 'scripts').mkdir()
    shutil.copy(KIT / 'tools' / 'cards.py', tmp_path / 'scripts' / 'cards.py')
    import subprocess, sys
    p = subprocess.run([sys.executable, 'scripts/cards.py', 'index', '--root', 'world'],
                       cwd=tmp_path, capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    index = (tmp_path / 'world/INDEX.md').read_text()
    assert 'Built by `scripts/cards.py index`' in index
    assert '`python3 scripts/cards.py find WORDS`' in index
    assert 'tools/cards.py' not in index


def test_check_v_lists_keyword_the_text_uses(tmp_path):
    world(tmp_path, extra={'world/places/the-light.md': card(
        'The Light', 'the lamp on the holm', kw='lantern, beacon', body='The lantern burns oil.')})
    run('cards', 'build', '--root', 'world', cwd=tmp_path)
    code, out = run('cards', 'check', '-v', '--root', 'world', cwd=tmp_path)
    assert 'world/places/the-light.md: keyword already in the text: lantern' in out.splitlines()
    assert 'beacon' not in out
    assert out.strip().splitlines()[-1] == '0 card problems'


def test_find_head_before_text(tmp_path):
    world(tmp_path, extra={'world/places/saltby.md': card(
        'Saltby', 'the village', kw='harbor', body='Boats leave for the skerry at dawn.')})
    code, out = run('cards', 'find', 'skerry', '--root', 'world', cwd=tmp_path)
    assert out.splitlines() == [
        'world/places/bell-rock.md: Bell Rock: a reef off the holm',
        'world/places/saltby.md: Saltby: the village (in the text)',
    ]
    code, out = run('cards', 'find', 'kraken', '--root', 'world', cwd=tmp_path)
    assert out.strip() == 'no card'
