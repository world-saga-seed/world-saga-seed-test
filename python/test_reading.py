"""reading.py: one chapter's reading list, one hop from its outline and notes.

The cases plant a linked card (listed whole), a link with an #anchor into a
large file (listed by that section's line range), a card named only by a
keyword and one by a person's first name (both found without a link), a card
nobody names (left out), a character sheet named by first name, the chapter
before in prose (a later chapter is not), a link to another outline (listed as
not to read), --step narrowing the list, --digest, --large, and a chapter with
no outline (exits with a message).
"""
from conftest import run, write


def card(name, what, kw, body='Text.'):
    return f'# {name}: {what}\n\n*Summary.*\n\nKeywords: {kw}\n\n{body}\n'


BIG = ('# The Light: the lamp room\n\n*Summary.*\n\nKeywords: lamp\n\n'
       '## Wicks\n\nTrim them square and short each dusk.\n\n'
       '## Oil\n\nColza oil, kept warm in winter.\n')


def small_book(tmp_path):
    return write(tmp_path, {
        'story/outline/00500-the-inspector.md': (
            '# 00500 The inspector\n\n'
            '- Agnes and Wren at [the light](../../world/things/the-light.md#oil).\n'
            '- The [log](../../world/things/the-log.md) is written up.\n'
            '- Out past the reef the boats wait.\n'
            '- See [the arc](1-arc.md).\n'),
        'story/outline/1-arc.md': '# The arc\n',
        'story/notes/00500-the-inspector.md': '# Notes\n\n- Dell rows the inspector over.\n',
        'world/things/the-light.md': BIG,
        'world/things/the-log.md': card('The Log', 'the keeper\'s book', 'ledger'),
        'world/places/bell-rock.md': card('Bell Rock', 'a skerry', 'reef, breakers'),
        'world/people/dell-harker.md': card('Dell Harker', 'the ferryman', 'boatman'),
        'world/people/mary-quill.md': card('Mary Quill', 'the post woman', 'letters'),
        'world/README.md': '# World\n',
        'story/notes/characters/wren.md': '# Wren Ashby: the narrator\n\n## At a glance\n\nThirteen.\n\n## Habits\n\nCounts steps.\nHums.\n',
        'story/notes/characters/tom.md': '# Tom Pike: a boy\n',
        'story/prose/00400-the-forty-minutes.md': '# 00400\n\nProse.\n',
        'story/prose/00300-earlier.md': '# 00300\n\nProse.\n',
        'story/prose/00600-later.md': '# 00600\n\nProse.\n',
        'story/voice/voice.md': '# Voice\n',
        'story/volume/1-digest.md': '# Digest\n',
    })


def section(out, title):
    return out.split(f'## {title}\n', 1)[1].split('\n## ', 1)[0].strip().splitlines()


def test_smoke_on_the_book(book):
    code, out = run('reading', '00400', cwd=book)
    assert code == 0
    assert out.startswith('# Reading list for 00400 (drafter)\n')
    assert '- `story/outline/00400-the-forty-minutes.md` (whole)' in out
    assert '`story/outline/1-spring-tides.md`' in section(out, 'Linked but not to read')
    assert any(l.startswith('- `story/notes/characters/wren.md`') for l in section(out, 'People'))


def test_drafter_list(tmp_path):
    small_book(tmp_path)
    code, out = run('reading', '00500', '--large', '20', cwd=tmp_path)
    assert code == 0
    assert section(out, 'Rules') == ['- `story/voice/voice.md`', '- two or three of `story/voice/samples/`']
    assert section(out, 'The chapter') == ['- `story/outline/00500-the-inspector.md` (whole)',
                                           '- `story/notes/00500-the-inspector.md` (whole)']
    cards = section(out, 'Cards and sections')
    assert cards[0].startswith('- `world/things/the-light.md` (')                 # by link, one section
    assert cards[0].endswith(' words in all; read only these sections, by line):')
    assert cards[1].startswith('  - lines 11 to 14: "Oil" (8 words)')
    assert cards[2].startswith('- `world/things/the-log.md` (whole, ')
    assert len(cards) == 3
    # named without a link (Dell, by first name): listed apart, not to read
    assert section(out, 'Named but not linked')[-1] == '`world/people/dell-harker.md`'
    # a keyword ("reef") is a search word, not a name: no longer pulls a card in
    assert 'bell-rock' not in out
    assert 'mary-quill' not in out and 'README' not in out
    assert section(out, 'Linked but not to read')[-1] == '`story/outline/1-arc.md`'
    people = section(out, 'People')
    assert len(people) == 1 and people[0].startswith('- `story/notes/characters/wren.md` (whole, ')
    assert section(out, 'Prose') == ['- `story/prose/00400-the-forty-minutes.md`: the chapter before; read closely']


def test_large_default_lists_small_file_whole(tmp_path):
    small_book(tmp_path)
    code, out = run('reading', '00500', cwd=tmp_path)
    assert any(l.startswith('- `world/things/the-light.md` (whole, ') for l in section(out, 'Cards and sections'))
    assert 'lines 11 to 14' not in out


def test_digest(tmp_path):
    small_book(tmp_path)
    code, out = run('reading', '00500', '--digest', 'story/volume/1-digest.md', cwd=tmp_path)
    assert section(out, 'Prose')[0] == ("- `story/volume/1-digest.md`: what the volume's pages have already set; "
                                        'read whole, in place of the earlier chapters')


def test_step_habits_lists_only_the_habits_section(tmp_path):
    small_book(tmp_path)
    code, out = run('reading', '00500', '--step', 'habits', cwd=tmp_path)
    assert out.startswith('# Reading list for 00500 (habits)\n')
    assert '## Rules' not in out and '## Cards and sections' not in out and '## Prose' not in out
    people = section(out, 'People')
    assert people[0].startswith('- `story/notes/characters/wren.md` (')
    assert people[1].startswith('  - lines 7 to 11: "Habits" (5 words)')


def test_step_continuity_lists_only_prose(tmp_path):
    small_book(tmp_path)
    code, out = run('reading', '00500', '--step', 'continuity', cwd=tmp_path)
    heads = [l for l in out.splitlines() if l.startswith('## ')]
    assert heads == ['## The chapter', '## Prose']


def test_no_outline_exits_with_message(tmp_path):
    small_book(tmp_path)
    code, out = run('reading', '00900', cwd=tmp_path)
    assert (code, out.strip()) == (1, 'no outline or notes for 00900')


def test_named_read_puts_named_cards_with_the_linked(tmp_path):
    small_book(tmp_path)
    code, out = run('reading', '00500', '--named', 'read', cwd=tmp_path)
    assert any(l.startswith('- `world/people/dell-harker.md` (whole, ') for l in section(out, 'Cards and sections'))
    assert '## Named but not linked' not in out


def test_named_off_leaves_them_out(tmp_path):
    small_book(tmp_path)
    code, out = run('reading', '00500', '--named', 'off', cwd=tmp_path)
    assert 'dell-harker' not in out


def test_a_sheets_subfolder_counts_only_when_linked(tmp_path):
    small_book(tmp_path)
    write(tmp_path, {'story/notes/characters/wren/backstory.md': '# Wren Ashby: backstory\n\nLong.\n'})
    code, out = run('reading', '00500', cwd=tmp_path)
    assert 'wren/backstory' not in out


def test_drafter_and_setup_read_the_sheet_sections_of_a_long_sheet(tmp_path):
    small_book(tmp_path)
    long = ('# Wren Ashby: the narrator\n\n## At a glance\n\nThirteen.\n\n## Backstory\n\n' + 'word ' * 60 +
            '\n\n## Habits\n\nCounts steps.\n')
    write(tmp_path, {'story/notes/characters/wren.md': long})
    for step in ('drafter', 'setup'):
        code, out = run('reading', '00500', '--step', step, '--large', '20', cwd=tmp_path)
        people = '\n'.join(section(out, 'People'))
        assert '"At a glance"' in people and '"Habits"' in people and 'Backstory' not in people, step


def test_sheet_budget_caps_the_sections(tmp_path):
    small_book(tmp_path)
    long = '# Wren Ashby: the narrator\n\n## At a glance\n\n' + 'word ' * 30 + '\n\n## Habits\n\n' + 'step ' * 30 + '\n'
    write(tmp_path, {'story/notes/characters/wren.md': long})
    code, out = run('reading', '00500', '--large', '20', '--sheet-budget', '40', cwd=tmp_path)
    people = '\n'.join(section(out, 'People'))
    assert '"At a glance"' in people and '"Habits"' not in people


def test_a_sheet_with_no_sections_is_its_head_counted_right(tmp_path):
    small_book(tmp_path)
    write(tmp_path, {'story/notes/characters/wren.md': '# Wren Ashby: the narrator\n\n' + 'word ' * 30 + '\n- **Habits.** Hums.\n'})
    code, out = run('reading', '00500', '--large', '20', cwd=tmp_path)
    assert '- `story/notes/characters/wren.md`: lines 1 to 4 (the head) and the **Habits.** item' in out


def test_sections_covering_nearly_the_whole_file_are_the_whole_file(tmp_path):
    small_book(tmp_path)
    big = '# The Light: the lamp room\n\n*S.*\n\nKeywords: lamp\n\n## Oil\n\n' + 'oil ' * 100 + '\n'
    write(tmp_path, {'world/things/the-light.md': big})
    code, out = run('reading', '00500', '--large', '20', cwd=tmp_path)
    assert any(l.startswith('- `world/things/the-light.md` (whole, ') for l in section(out, 'Cards and sections'))


def test_not_before_skips_fragments_for_the_chapter_before(tmp_path):
    small_book(tmp_path)
    write(tmp_path, {'story/prose/00450-F1-a-fragment.md': '# F\n'})
    code, out = run('reading', '00500', '--not-before=-F[0-9]', cwd=tmp_path)
    assert '00400-the-forty-minutes.md`: the chapter before' in out
    assert '- `story/prose/00450-F1-a-fragment.md`: kept between the chapter before and this one; skim' in out
    code, out = run('reading', '00500', cwd=tmp_path)
    assert '00450-F1-a-fragment.md`: the chapter before' in out


def test_samples_and_rules_options(tmp_path):
    small_book(tmp_path)
    code, out = run('reading', '00500', '--samples', 'voice/mine/', '--rules', 'story/voice/voice.md', cwd=tmp_path)
    assert section(out, 'Rules') == ['- `story/voice/voice.md`', '- two or three of `voice/mine/`']


def test_linked_prose_is_not_in_the_unread_list(tmp_path):
    small_book(tmp_path)
    write(tmp_path, {'story/notes/00500-the-inspector.md': '# Notes\n\n- As in [00300](../prose/00300-earlier.md).\n'})
    code, out = run('reading', '00500', cwd=tmp_path)
    assert '00300-earlier' not in '\n'.join(section(out, 'Linked but not to read'))


def test_the_unread_list_names_only_outlines_and_notes(tmp_path):
    small_book(tmp_path)
    write(tmp_path, {'story/notes/00500-the-inspector.md': '# Notes\n\n- By [the voice](../voice/voice.md) and [the plan](../volume/plan.md).\n',
                     'story/volume/plan.md': '# Plan\n'})
    code, out = run('reading', '00500', '--step', 'facts', cwd=tmp_path)
    unread = '\n'.join(section(out, 'Linked but not to read'))
    assert 'voice.md' not in unread and 'plan.md' not in unread and '1-arc.md' in unread


FIELDED = ('# Selkie: a beast\n\n*Summary.*\n\nKeywords: seal\n\n## Selkie\n\n'
           '- **Body.** *(Settled, [R0302-01](../../plan/l.md).)* Grey. *(Proposal.)* Spotted when young.\n'
           '- **Threat.** *(Proposal.)* Bites when cornered.\n'
           '- **Size.** *(Settled.)* Two arms long.\n'
           '- **Origin and lineage.** *(Settled.)* From the north.\n'
           '- **Appears in.** 00400.\n')


def bundle_book(tmp_path, notes='# Notes\n\n- Dell rows the inspector over.\n'):
    small_book(tmp_path)
    return write(tmp_path, {
        'world/beast/selkie.md': FIELDED,
        'story/outline/00500-the-inspector.md': '# 00500\n\n- Wren sees a [selkie](../../world/beast/selkie.md) in the harbour, '
                                                'at [the light](../../world/things/the-light.md#oil).\n',
        'story/notes/00500-the-inspector.md': notes,
        'aliases.tsv': 'size\tworld/beast\tSize; Body\n'})


def test_bundle_prints_the_text_not_a_list(tmp_path):
    bundle_book(tmp_path)
    code, out = run('reading', '00500', '--step', 'drafter', '--bundle', '--large', '20', cwd=tmp_path)
    assert out.startswith('# Reading for 00500 (drafter)')
    assert '### Selkie (beast)' in out and 'Spotted when young' in out   # the drafter keeps proposals, and gets no path
    assert '](../../' not in out                                                           # link targets cut
    assert '(Settled' in out                                                               # marks kept: it must know what is settled
    assert 'Origin and lineage' not in out and 'Appears in.' not in out                    # bookkeeping cut
    assert 'Colza oil' in out and 'Trim them square' not in out                            # the linked section only


def test_bundle_facts_is_settled_text_with_annotations_cut(tmp_path):
    bundle_book(tmp_path)
    code, out = run('reading', '00500', '--step', 'facts', '--bundle', cwd=tmp_path)
    assert '- **Body.** Grey.' in out and 'Spotted' not in out and 'Bites' not in out
    assert 'R0302' not in out and '*(' not in out
    assert 'Only settled text; cut: link targets, marks, ruling IDs.' in out


def test_bundle_scale_asks_sizes_through_the_aliases(tmp_path):
    bundle_book(tmp_path)
    code, out = run('reading', '00500', '--step', 'scale', '--bundle', '--aliases', 'aliases.tsv', cwd=tmp_path)
    sel = out.split('### Selkie', 1)[1].split('###', 1)[0]
    assert sel.index('**Size.**') < sel.index('**Body.**') and 'Threat' not in sel
    assert 'The Light' not in out                     # a card of sections answers no size question


def test_bundle_an_include_names_the_fields_the_chapter_needs(tmp_path):
    bundle_book(tmp_path, notes='# Notes\n\n## Cards\n\n- [Selkie](../../world/beast/selkie.md): Size\n')
    code, out = run('reading', '00500', '--step', 'drafter', '--bundle', cwd=tmp_path)
    sel = out.split('### Selkie', 1)[1].split('###', 1)[0]
    assert 'Size: ' in sel and 'Body: ' not in sel


def test_bundle_recipes_file_overrides_a_role(tmp_path):
    bundle_book(tmp_path)
    write(tmp_path, {'recipes.tsv': 'facts\tThreat\tnone\tno\tlinks\n'})
    code, out = run('reading', '00500', '--step', 'facts', '--bundle', '--recipes', 'recipes.tsv', cwd=tmp_path)
    sel = out.split('### Selkie', 1)[1]
    assert 'Bites when cornered' in sel and '**Body.**' not in sel and '## People' not in out


def test_bundle_a_long_sheet_without_sections_gives_its_head_and_habits(tmp_path):
    bundle_book(tmp_path)
    write(tmp_path, {'story/notes/characters/wren.md':
                     '# Wren Ashby: the narrator\n\n*S.*\n\nKeywords: k\n\nThe narrator.\n- **Who.** A keeper\'s granddaughter.\n'
                     '- **Habits.** Counts steps.\n- **Backstory.** ' + 'long ' * 60 + '\n'})
    code, out = run('reading', '00500', '--step', 'drafter', '--bundle', '--large', '20', cwd=tmp_path)
    w = out.split('### Wren Ashby', 1)[1]
    assert 'Counts steps' in w and "granddaughter" in w and 'long long' not in w


def test_bundle_sheet_sections_are_not_given_twice(tmp_path):
    bundle_book(tmp_path)
    write(tmp_path, {'story/notes/characters/wren.md':
                     '# Wren Ashby: the narrator\n\n## Personality and voice\n\nShy.\n\n### How she talks\n\nShort.\n\n'
                     '## Backstory\n\n' + 'long ' * 60 + '\n'})
    code, out = run('reading', '00500', '--step', 'drafter', '--bundle', '--large', '20', cwd=tmp_path)
    assert out.count('Short.') == 1


def test_bundle_inline_puts_the_chapter_in_cut_for_the_drafter(tmp_path):
    bundle_book(tmp_path, notes=('# Notes\n\n[arc](1-arc.md) · [previous](00400-a.md) · [next](00600-b.md)\n\n'
                                 '## What the scene does\n\n'
                                 '- *(Settled, R0302-07.)* Dell rows the inspector over ([the harbour card](../../world/beast/selkie.md), 3).\n'
                                 '- ~~Dell sings.~~ *(Withdrawn.)* Dell hums.\n'
                                 '- *(Author-side.)* The selkie is the inspector\'s sister.\n\n'
                                 '## Author-side only\n\n- The ending is a dream.\n\n'
                                 '## Cards\n\n- [selkie](../../world/beast/selkie.md): Size\n'))
    code, out = run('reading', '00500', '--step', 'drafter', '--bundle', '--inline', '--large', '20', cwd=tmp_path)
    notes = out.split('## Notes\n', 1)[1].split('\n## Cards', 1)[0]
    assert 'Dell rows the inspector over.' in notes and '*(Settled.)*' in notes   # mark kept, its ID and the citation cut
    assert 'harbour card' not in notes and 'previous' not in notes               # source citation and navigation cut
    assert 'Dell sings' not in notes and 'Dell hums.' in notes                    # struck text is withdrawn
    assert 'sister' not in notes and 'dream' not in notes                         # author-side items and sections
    assert '## The chapter (read these files)' not in out
    assert '### Selkie' in out                                                    # the include still resolves


def test_bundle_drafter_drops_author_side_text_the_critics_keep_it(tmp_path):
    bundle_book(tmp_path)
    sheet = ('# Wren Ashby: the narrator\n\n## At a glance\n\n'
             '- **Who.** *(Settled.)* The lamp keeper\'s girl. *(Settled, author-side.)* She is the inspector\'s heir.\n'
             '- **Count.** *(Settled; the count author-side.)* She keeps three lamps lit.\n'
             '- **Gag.** *(Settled: the writer\'s line; it is author-side commentary.)* Lamps, but make it fashion.\n'
             '\n## Habits\n\n- Trims wicks square.\n')
    write(tmp_path, {'story/notes/characters/wren.md': sheet})
    code, out = run('reading', '00500', '--step', 'drafter', '--bundle', '--large', '20', cwd=tmp_path)
    assert "lamp keeper's girl" in out and 'heir' not in out          # the author-side passage only
    assert 'three lamps lit' in out                                     # only the figure is author-side
    assert 'fashion' not in out
    code, out = run('reading', '00500', '--step', 'setup', '--bundle', '--large', '20', cwd=tmp_path)
    assert 'heir' in out                                                # a critic checks against it


def test_bundle_includes_only_under_cards_and_cited_is_not_read(tmp_path):
    bundle_book(tmp_path, notes=('# Notes\n\n## What the scene does\n\n'
                                 '- [selkie](../../world/beast/selkie.md): seen once, far off.\n'   # a note, not an include
                                 '\n## Cards\n\n- [the light](../../world/things/the-light.md#oil): cited\n'))
    code, out = run('reading', '00500', '--step', 'drafter', '--bundle', '--large', '20', cwd=tmp_path)
    assert 'Spotted when young' in out          # the note line did not narrow the selkie to a field "seen once"
    assert 'Colza oil' not in out               # cited: the source is not read


SO_FAR = ('# Selkie: a beast\n\n*Summary.*\n\nKeywords: seal\n\n## Selkie\n\n'
          '- **Body.** *(Settled.)* Grey, a man\'s length (00300:12). It sheds in the cold (00700). "Out of the water at last," he said ([00700](../../story/prose/00700-x.md):4).\n'
          '- **On the page.** *(Proposal.)* Seen on the rocks.\n'
          '  - At the slip, a pup ([00200](../../story/prose/00200-a.md):9).\n'
          '  - At the wreck, a bull (00900:3). *(Settled: from 00900 (a later chapter).)*\n'
          '- **Threat.** Bites. 00200 00400 00800 (M7)\n'
          '- **Size.** *(Settled.)* As long as a boat, see notes.md.\n')


def test_bundle_drafter_gets_only_the_book_so_far_with_no_paths(tmp_path):
    bundle_book(tmp_path)
    write(tmp_path, {'world/beast/selkie.md': SO_FAR})
    code, out = run('reading', '00500', '--step', 'drafter', '--bundle', '--large', '20', cwd=tmp_path)
    cards = out.split('## Cards', 1)[1].split('\n## ', 1)[0]
    assert '### Selkie (beast)' in cards and 'world/' not in cards and '.md' not in cards
    assert "Body: (Settled.) Grey, a man's length." in cards                  # field form, citation cut
    assert 'It sheds in the cold.' in cards                                   # a trait: where it is shown, not when it is true
    assert 'Out of the water' not in cards                                    # a later chapter's page
    assert 'a pup' in cards and 'a bull' not in cards and 'later chapter' not in cards
    assert 'Threat: Bites.' in cards and '00400' not in cards and 'M7' not in cards
    assert 'search for nothing else' in out and '## Named but not linked' not in out
    code, out = run('reading', '00500', '--step', 'facts', '--bundle', '--large', '20', cwd=tmp_path)
    assert 'world/beast/selkie.md' in out                                     # a critic keeps the path


def test_bundle_drafter_chapter_headings_and_text_carry_no_paths(tmp_path):
    bundle_book(tmp_path, notes='# Notes\n\n## Reread plants\n\n- `"Lamp," she said.` (`prose/00500-the-inspector.md:10`) a clue.\n')
    code, out = run('reading', '00500', '--step', 'drafter', '--bundle', '--inline', '--large', '20', cwd=tmp_path)
    assert '## Notes\n' in out and '00500-the-inspector.md' not in out
    assert '"Lamp," she said.' in out and 'a clue.' in out                    # the clue stays


def test_bundle_manifest_records_what_each_file_gave(tmp_path):
    bundle_book(tmp_path, notes='# Notes\n\n## Cards\n\n- [Selkie](../../world/beast/selkie.md): Size\n'
                                '- [The Log](../../world/things/the-log.md): cited\n')
    code, out = run('reading', '00500', '--step', 'drafter', '--bundle', '--manifest', 'man.tsv', cwd=tmp_path)
    man = (tmp_path / 'man.tsv').read_text()
    assert '# commit ' in man                              # the commit it was built at, for uses.py
    rows = dict(l.split('\t', 1) for l in man.split('\n') if '\t' in l and not l.startswith('#'))
    assert rows['world/beast/selkie.md'] == 'fields: Size'
    assert 'not given' in rows['world/things/the-log.md']


def test_bundle_called_heads_a_card_by_its_page_name(tmp_path):
    bundle_book(tmp_path)
    write(tmp_path, {'called.tsv': 'world/beast/selkie.md\tthe grey thing; Old Grey\n'})
    code, out = run('reading', '00500', '--step', 'drafter', '--bundle', '--called', 'called.tsv', cwd=tmp_path)
    assert '### the grey thing, Old Grey (beast)' in out and '### Selkie' not in out


def test_bundle_drafter_cuts_fields_that_look_ahead(tmp_path):
    bundle_book(tmp_path)
    write(tmp_path, {'world/beast/selkie.md': FIELDED.replace('- **Appears in.**',
                     '- **In volume 3.** *(Settled.)* It is a man under the skin.\n- **Open.** Its call.\n- **Appears in.**')})
    code, out = run('reading', '00500', '--step', 'drafter', '--bundle', cwd=tmp_path)
    assert 'Two arms long' in out and 'under the skin' not in out and 'Its call' not in out
    code, out = run('reading', '00500', '--step', 'facts', '--bundle', cwd=tmp_path)
    assert 'under the skin' in out                       # the critics keep it, to check the page against


def test_suggest_lists_named_and_keyword_cards_not_linked(tmp_path):
    bundle_book(tmp_path, notes='# Notes\n\n- Dell rows the inspector over; the keeper writes in his ledger.\n')
    code, out = run('reading', '00500', '--suggest', cwd=tmp_path)
    assert code == 0 and out.startswith('# Includes to consider for 00500')
    assert '[Dell Harker](' in out and 'named' in out          # a person named by first name
    assert '[The Log](' in out and 'keywords: ledger' in out   # a keyword match
    assert '[Selkie](' not in out                              # linked already: not a suggestion
    assert '[Mary Quill](' not in out
