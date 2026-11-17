"""cards.py fields and get: each kind's fields checked against a forms file, and
fields asked for by name, by question, settled only, with annotations cut."""
from conftest import run, write

HEAD = '# {n}: {w}\n\n*Summary.*\n\nKeywords: {k}\n\n## {n}\n\n'
FORMS = ('# kind\tfields\n'
         'world/beast\tBody; Size?; Threat; Name; Open?\n')
ALIASES = 'size\tworld/beast\tSize; Body\ndanger\tworld/beast\tThreat\n'


def beast(name, body, kw='seal'):
    return HEAD.format(n=name, w='a beast', k=kw) + body


def book(tmp_path, extra=None):
    files = {
        'forms.tsv': FORMS, 'aliases.tsv': ALIASES,
        'world/README.md': '# World\n',
        'world/beast/README.md': '# Beasts\n\n<!-- cards: built -->\n<!-- /cards -->\n',
        'world/beast/selkie.md': beast('Selkie',
            '- **Body.** *(Settled, R0302-01.)* Grey, a man\'s length. *(Proposal.)* Spotted when young.\n'
            '- **Size.** *(Settled by the writer, [R0302-02](../../plan/ledger.md).)* Two arms long.\n'
            '- **Threat.** *(Proposal.)* Bites when cornered.\n'
            '- **Name.** Selkie.\n'
            '- **Moods.** Sulks in fog.\n'
            '\n## Later\n\n- **Shore.** Bold items here are content, not fields.\n'),
        'world/beast/gull.md': beast('Gull', '- **Name.** Gull.\n- **Body.** White.\n', kw='bird, harbour'),
    }
    files.update(extra or {})
    return write(tmp_path, files)


def test_fields_reports_missing_and_order_not_a_cards_own_field(tmp_path):
    book(tmp_path)
    code, out = run('cards', 'fields', 'forms.tsv', cwd=tmp_path)
    assert code == 1
    assert 'world/beast/gull.md: missing field: Threat' in out
    assert 'world/beast/gull.md: fields out of order: Name, Body' in out
    assert 'missing field: Size' not in out and 'missing field: Open' not in out   # optional
    assert 'world/beast/selkie.md: (info) a field of its own: Moods' in out
    assert 'Shore' not in out                                                        # after the second heading
    assert out.strip().splitlines()[-1].startswith('2 field problems; 1 fields of their own')


def test_fields_passes_a_card_in_form(tmp_path):
    book(tmp_path, {'world/beast/gull.md': beast('Gull', '- **Body.** White.\n- **Threat.** Low.\n- **Name.** Gull.\n')})
    code, out = run('cards', 'fields', 'forms.tsv', cwd=tmp_path)
    assert code == 0 and out.strip().splitlines()[-1].startswith('0 field problems')


def test_get_fields_by_name_in_the_order_asked(tmp_path):
    book(tmp_path)
    code, out = run('cards', 'get', 'selkie', '--fields', 'Threat,Body', cwd=tmp_path)
    assert '## Selkie (world/beast/selkie.md)' in out
    body = out.split('## Selkie', 1)[1]
    assert body.index('**Threat.**') < body.index('**Body.**')
    assert '**Name.**' not in body


def test_get_by_question_through_the_aliases(tmp_path):
    book(tmp_path)
    code, out = run('cards', 'get', 'Selkie', '--fields', 'size', '--aliases', 'aliases.tsv', cwd=tmp_path)
    body = out.split('## Selkie', 1)[1]
    assert body.index('**Size.**') < body.index('**Body.**') and 'Threat' not in body


def test_get_settled_drops_proposed_text_and_a_field_left_empty(tmp_path):
    book(tmp_path)
    code, out = run('cards', 'get', 'selkie', '--settled', cwd=tmp_path)
    assert "Grey, a man's length." in out and 'Spotted when young' not in out
    assert 'Bites when cornered' not in out and '**Threat.**' not in out
    assert '- **Name.** Selkie.' in out                                     # unmarked text is kept
    assert out.splitlines()[0] == '*only settled text. The full card is at its path.*'


def test_get_strip_cuts_links_marks_and_ids(tmp_path):
    book(tmp_path)
    code, out = run('cards', 'get', 'selkie', '--fields', 'Size', '--strip', 'links,marks,ids', cwd=tmp_path)
    assert '- **Size.** Two arms long.' in out
    assert 'R0302' not in out and '](' not in out and '*(' not in out
    assert 'cut: link targets, marks, ruling IDs' in out.splitlines()[0]


def test_get_strip_links_keeps_the_words(tmp_path):
    book(tmp_path)
    code, out = run('cards', 'get', 'selkie', '--fields', 'Size', '--strip', 'links', cwd=tmp_path)
    assert 'R0302-02' in out and '../../plan' not in out


def test_get_by_keyword_and_section(tmp_path):
    book(tmp_path)
    code, out = run('cards', 'get', '--keyword', 'harbour', cwd=tmp_path)
    assert '## Gull (world/beast/gull.md)' in out and 'Selkie' not in out
    code, out = run('cards', 'get', 'selkie#later', cwd=tmp_path)
    assert '## Selkie (world/beast/selkie.md#later)' in out and 'Bold items here are content' in out


def test_get_unknown_card_says_so(tmp_path):
    book(tmp_path)
    code, out = run('cards', 'get', 'kraken', cwd=tmp_path)
    assert 'Kraken' not in out


def test_get_table_a_row_per_card_a_column_per_question(tmp_path):
    book(tmp_path)
    code, out = run('cards', 'get', 'selkie', 'gull', '--table', '--fields', 'size,danger',
                    '--aliases', 'aliases.tsv', '--strip', 'links,marks,ids', cwd=tmp_path)
    lines = out.strip().splitlines()
    assert lines[0] == '| Card | size | danger |'
    selkie = next(l for l in lines if l.startswith('| [Selkie]'))
    assert 'Two arms long.' in selkie and 'Grey' in selkie and 'Bites when cornered.' in selkie
    assert 'R0302' not in selkie and 'Proposal' not in selkie
    gull = next(l for l in lines if l.startswith('| [Gull]'))
    assert gull.endswith('| — |')            # no Threat on the gull: a dash, not a gap


def test_get_table_with_no_fields_is_a_brief_index_cut_to_cell(tmp_path):
    book(tmp_path, {'world/beast/gull.md': beast('Gull', '- **Name.** Gull, | a pipe, ' + 'word ' * 50 + '\n')})
    code, out = run('cards', 'get', 'gull', '--table', '--cell', '5', cwd=tmp_path)
    row = next(l for l in out.splitlines() if l.startswith('| [Gull]'))
    assert '\\|' in row and row.endswith('… |') and 'First field' in out


SHEET = ('# Wren: a sheet\n\n*Summary.*\n\nKeywords: wren\n\n## Wren\n\n- **Body.** Small.\n- **Name.** Wren.\n\n'
         '## Looks\n\n- Brown, quick.\n\n## Voice\n\n- Sings at dawn.\n\n## Later\n\n- Not asked.\n')


def test_sections_map_counts_a_field_held_in_sections_and_get_pulls_them(tmp_path):
    book(tmp_path, {'world/beast/wren.md': SHEET,
                    'sections.tsv': '# card\tfield\tsources\nworld/beast/wren.md\tThreat\tLooks; Voice\n'})
    code, out = run('cards', 'fields', 'forms.tsv', '--sections', 'sections.tsv', cwd=tmp_path)
    assert 'wren.md: missing field: Threat' not in out
    code, out = run('cards', 'get', 'wren', '--fields', 'Threat', '--sections', 'sections.tsv', cwd=tmp_path)
    assert '## Looks' in out and 'Sings at dawn.' in out and 'Not asked.' not in out


def test_sections_map_own_label_dash_and_a_missing_section(tmp_path):
    book(tmp_path, {'world/beast/gull.md': beast('Gull', '- **Body.** White.\n- **Danger.** Steals chips.\n- **Name.** Gull.\n'),
                    'world/beast/wren.md': SHEET,
                    'sections.tsv': 'world/beast/gull.md\tThreat\t**Danger**\n'
                                    'world/beast/wren.md\tThreat\t-\n'
                                    'world/beast/selkie.md\tOpen\tNo such heading\n'})
    code, out = run('cards', 'fields', 'forms.tsv', '--sections', 'sections.tsv', cwd=tmp_path)
    assert 'gull.md: missing field: Threat' not in out and 'a field of its own: Danger' not in out
    assert 'wren.md: missing field: Threat' not in out                # does not apply
    assert 'selkie.md: Open is mapped to a section the card lacks: No such heading' in out
    code, out = run('cards', 'get', 'gull', '--table', '--fields', 'Threat', '--sections', 'sections.tsv', cwd=tmp_path)
    assert 'Steals chips.' in out
