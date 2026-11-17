"""uses.py: when a card changes, the drafted chapters whose bundle gave what changed, and their lines that name it."""
import subprocess
from conftest import run, write

CARD = ('# Selkie: a beast\n\n*Summary.*\n\nKeywords: seal, harbour-seal\n\n## Selkie\n\n'
        '- **Body.** Grey.\n- **Size.** Two arms long.\n')


def book(tmp_path):
    write(tmp_path, {
        'world/beast/selkie.md': CARD,
        'story/notes/characters/agnes.md': '# Agnes Ashby: the mother\n\n*S.*\n\nKeywords: keeper\n',
        'story/prose/00400-the-boat.md': '# 00400\n\nA selkie came up.\nNothing here.\nMy mother called.\n',
        'story/prose/00500-the-inspector.md': '# 00500\n\nThe harbour-seal was grey.\n',
        'story/prose/00600-later.md': '# 00600\n\nThe selkie again.\n',
        'mans/00400-drafter.tsv': '# 00400\n# commit abc1234\nworld/beast/selkie.md\tfields: Size\n'
                                  'story/notes/characters/agnes.md\twhole\n',
        'mans/00500-drafter.tsv': '# 00500\n# commit abc1234\nworld/beast/selkie.md\tfields: Body\n',
        'mans/00600-drafter.tsv': '# 00600\n# commit abc1234\nworld/beast/selkie.md\tcited: not given\n',
        'called.tsv': 'story/notes/characters/agnes.md\tmy mother\n'})
    return tmp_path


def git(cwd, *a):
    subprocess.run(['git', *a], cwd=cwd, check=True, capture_output=True,
                   env={'GIT_AUTHOR_NAME': 't', 'GIT_AUTHOR_EMAIL': 't@t', 'GIT_COMMITTER_NAME': 't',
                        'GIT_COMMITTER_EMAIL': 't@t', 'PATH': '/usr/bin:/bin'})


def test_named_card_lists_every_chapter_that_was_given_it(tmp_path):
    book(tmp_path)
    code, out = run('uses', '--manifests', 'mans', 'world/beast/selkie.md', cwd=tmp_path)
    assert code == 0 and '## world/beast/selkie.md: whole card' in out
    assert '**00400**' in out and '00400-the-boat.md:3' in out
    assert '**00500**' in out and '00500-the-inspector.md:3' in out      # a Keywords word names it too
    assert 'not given to the drafter (cited, named, or other fields): 00600' in out


def test_since_lists_only_the_chapters_given_the_changed_field(tmp_path):
    book(tmp_path)
    git(tmp_path, 'init', '-q'); git(tmp_path, 'add', '-A'); git(tmp_path, 'commit', '-qm', 'base')
    (tmp_path / 'world/beast/selkie.md').write_text(CARD.replace('Two arms long.', 'Three arms long.'))
    code, out = run('uses', '--manifests', 'mans', '--since', 'HEAD', cwd=tmp_path)
    assert 'changed: Size' in out
    assert '**00400**' in out and 'given Size' in out
    assert '**00500**' not in out and '00500' in out.split('not given to the drafter')[1]


def test_called_finds_what_the_page_calls_a_person(tmp_path):
    book(tmp_path)
    card = 'story/notes/characters/agnes.md'
    code, out = run('uses', '--manifests', 'mans', card, cwd=tmp_path)
    assert '00400-the-boat.md:5' not in out
    code, out = run('uses', '--manifests', 'mans', card, '--called', 'called.tsv', cwd=tmp_path)
    assert '00400-the-boat.md:5' in out and 'My mother called.' in out
