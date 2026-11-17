"""context: pattern matches with their sentences or paragraphs around them.

Plants: a plain match with its window; a near pattern inside and outside the
distance; an unless rule (a ribbon with no colour beside it is not flagged, a
red one is); a match in dialogue skipped with --narration; paragraph windows
holding the two before; a quotation never split into sentences; merged windows;
a patterns file with per-line options; --fail for a guard; the summary table.
"""
from conftest import run, write, BOOK

CH = """# The ford (draft 1)

Wren came down to the ford at the ebb. The water was low. Agnes had the lamp.

"Mind the weed," Agnes said. "It is slick at the ebb. Slicker than you think."

Wren wore her blue ribbon. The causeway stones were dry. She did not look back.

Later the tide came in, and Wren tied a red ribbon to the post to mark the line.

## Notes

The ebb, the ribbon, noon.
"""


def chapter(tmp_path):
    write(tmp_path, {'00100-ford.md': CH})
    return '00100-ford.md'


def test_plain_match_prints_its_window_and_line(tmp_path):
    code, out = run('context', chapter(tmp_path), '--pattern', 'lamp=\\blamp\\b', cwd=tmp_path)
    assert code == 0
    assert '### 00100-ford.md:3  lamp  «lamp»' in out
    assert '> 3: Agnes had the lamp.' in out
    assert '  3: The water was low.' in out               # two sentences before, by default
    assert '**Total:** 1 matches' in out


def test_notes_section_is_not_read(tmp_path):
    code, out = run('context', chapter(tmp_path), '--pattern', 'noon=\\bnoon\\b', cwd=tmp_path)
    assert '**Total:** 0 matches' in out


def test_near_inside_and_outside_the_distance(tmp_path):
    f = chapter(tmp_path)
    _, out = run('context', f, '--pattern', 'ribbon=\\bribbon\\b', '--near', '\\bred\\b', '--within', '3', cwd=tmp_path)
    assert ':9  ribbon' in out and ':7  ribbon' not in out
    _, out = run('context', f, '--pattern', 'ribbon=\\bribbon\\b', '--near', '\\bpost\\b', '--within', '1', cwd=tmp_path)
    assert '**Total:** 0 matches' in out                 # "post" is three words off


def test_unless_flags_only_the_rule_broken(tmp_path):
    # a rule: ribbons are blue; a ribbon with "blue" beside it passes, the red one is flagged
    _, out = run('context', chapter(tmp_path), '--pattern', 'ribbon=\\bribbon\\b', '--unless', '\\bblue\\b', '--within', '2', cwd=tmp_path)
    assert ':9  ribbon' in out and ':7  ribbon' not in out and '**Total:** 1 matches' in out


def test_narration_skips_dialogue_but_keeps_it_in_the_window(tmp_path):
    f = chapter(tmp_path)
    _, out = run('context', f, '--pattern', 'ebb=\\bebb\\b', cwd=tmp_path)
    assert ':5  ebb' in out
    _, out = run('context', f, '--pattern', 'ebb=\\bebb\\b', '--narration', '--after', '3', cwd=tmp_path)
    assert ':5  ebb' not in out and ':3  ebb' in out
    assert '"Mind the weed," Agnes said.' in out          # dialogue still shown as context


def test_a_quotation_is_never_split(tmp_path):
    _, out = run('context', chapter(tmp_path), '--pattern', 'weed=\\bweed\\b', cwd=tmp_path)
    assert '> 5: "Mind the weed," Agnes said.' in out
    assert '"It is slick at the ebb. Slicker than you think."' in out


def test_para_window_holds_the_paragraphs_before(tmp_path):
    _, out = run('context', chapter(tmp_path), '--pattern', 'red=\\bred\\b', '--para', '2', cwd=tmp_path)
    assert '  5: "Mind the weed,"' in out and '  7: Wren wore her blue ribbon.' in out and '> 9: Later the tide' in out
    assert '  3: Wren came down' not in out


def test_merge_joins_overlapping_windows(tmp_path):
    f = chapter(tmp_path)
    _, out = run('context', f, '--pattern', 'w=\\bWren\\b', '--merge', '--before', '3', '--after', '3', cwd=tmp_path)
    assert out.count('### ') == 1 and '(also at 00100-ford.md:7' in out
    _, out = run('context', f, '--pattern', 'w=\\bWren\\b', cwd=tmp_path)
    assert out.count('### ') == 3


def test_patterns_file_with_options_and_fail(tmp_path):
    f = chapter(tmp_path)
    write(tmp_path, {'guards.tsv': "# guards\nred ribbon\t\\bribbon\\b\tunless=\\bblue\\b\twithin=2\nebb in narration\t\\bebb\\b\tnarration=1\n"})
    code, out = run('context', f, '--patterns', 'guards.tsv', '--fail', cwd=tmp_path)
    assert code == 1
    assert ':9  red ribbon' in out and ':3  ebb in narration' in out and ':5  ebb in narration' not in out
    code, out = run('context', f, '--pattern', 'gull=\\bgull\\b', '--fail', cwd=tmp_path)
    assert code == 0


def test_summary_counts_per_file_and_pattern(tmp_path):
    _, out = run('context', chapter(tmp_path), '--pattern', 'w=\\bWren\\b', '--pattern', 'a=\\bAgnes\\b', '--summary', cwd=tmp_path)
    assert '| 00100-ford.md | w | 3 |' in out and '| 00100-ford.md | a | 2 |' in out and '**Total:** 5 matches.' in out


def test_bad_input_exits_with_a_message(tmp_path):
    f = chapter(tmp_path)
    code, out = run('context', f, cwd=tmp_path)
    assert code != 0 and 'give --pattern or --patterns' in out
    code, out = run('context', f, '--pattern', 'nolabel', cwd=tmp_path)
    assert code != 0 and 'LABEL=REGEX' in out


def test_smoke_on_the_book():
    code, out = run('context', BOOK / 'story/prose/00400-the-forty-minutes.md', '--pattern', 'tide=\\btides?\\b', '--para', '1')
    assert code == 0 and '**Total:**' in out and '% of the' in out


def test_two_matches_in_a_paragraph_get_their_own_sentences(tmp_path):
    write(tmp_path, {'00200-x.md': '# X\n\nThe lady sat. Wren poured. Then the lady spoke, and the lady smiled.\n'})
    _, out = run('context', '00200-x.md', '--pattern', 'l=\\bthe lady\\b', '--before', '0', '--after', '0', cwd=tmp_path)
    assert out.count('### ') == 2                       # two sentences; the second holds two matches, one window
    assert '> 3: The lady sat.' in out and '> 3: Then the lady spoke, and the lady smiled.' in out


def test_tags_give_line_column_and_a_unique_anchor(tmp_path):
    f = chapter(tmp_path)
    _, out = run('context', f, '--pattern', 'r=\\bred ribbon\\b', '--tags', cwd=tmp_path)
    tag = next(l for l in out.splitlines() if l.startswith('@ '))
    assert tag.startswith('@ 00100-ford.md:9:41-50 anchor=«')
    a = tag.split('anchor=«', 1)[1].rstrip('»')
    text = (tmp_path / f).read_text()
    assert len(a.split()) >= 4 and text.count(a) == 1 and 'red ribbon' in a
    assert text.split('\n')[8][40:50] == 'red ribbon'


def test_anchor_grows_past_a_repeated_phrase(tmp_path):
    write(tmp_path, {'00300-y.md': '# Y\n\nAt the ebb the water was low.\n\nAt the ebb the water was low again.\n'})
    _, out = run('context', '00300-y.md', '--pattern', 'w=\\bwater\\b', '--tags', '--anchor-min', '2', cwd=tmp_path)
    tags = [l for l in out.splitlines() if l.startswith('@ ')]
    assert tags[0].startswith('@ 00300-y.md:3:') and 'not unique' not in tags[0]
    assert '«the water was low.' not in tags[0] or (tmp_path / '00300-y.md').read_text().count(tags[0].split('«')[1].rstrip('»')) == 1
    assert 'again' in tags[1]


def test_jsonl_is_one_record_per_match_and_total_on_stderr(tmp_path):
    import json, subprocess, sys
    from conftest import KIT
    f = chapter(tmp_path)
    p = subprocess.run([sys.executable, str(KIT / 'tools/context.py'), f, '--pattern', 'w=\\bWren\\b', '--jsonl'],
                       cwd=tmp_path, capture_output=True, text=True)
    recs = [json.loads(l) for l in p.stdout.splitlines()]
    assert len(recs) == 3 and '**Total:** 3 matches' in p.stderr
    lines = (tmp_path / f).read_text().split('\n')
    for r in recs:
        assert lines[r['line'] - 1][r['col'] - 1:r['end']] == 'Wren' and r['unique']
        assert any(w['hit'] for w in r['window'])
