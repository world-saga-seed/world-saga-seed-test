"""The prompt scorer (llm/score.py): planted faults matched by line, unmatched findings counted, the pass line applied."""
import subprocess, sys
from conftest import HERE, write

SCORE = HERE.parent / 'llm' / 'score.py'
KEY = """**Pass:** 2 of 3 caught, at most 1 unmatched.

| ID | Line | Kind | Plant |
|---|---|---|---|
| K1 | 10 | fact | the tide at six |
| K2 | 20-22 | voice | a modern word |
| K3 | 40 | logic | the lamp lit twice |
"""


def score(tmp_path, report, *args):
    write(tmp_path, {'key.md': KEY, 'report.md': report})
    p = subprocess.run([sys.executable, str(SCORE), 'key.md', 'report.md', *args], cwd=tmp_path, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def test_line_within_slack_and_range_catch(tmp_path):
    code, out = score(tmp_path, '- line 11: fact: the tide\n- L22 voice: "okay"\n')
    assert 'caught  K1' in out and 'caught  K2' in out and 'MISSED  K3' in out
    assert '2 of 3 caught, 0 unmatched' in out and out.rstrip().endswith('PASS') and code == 0


def test_far_line_is_unmatched_and_fails_the_limit(tmp_path):
    code, out = score(tmp_path, '- line 10: x\n- line 20: y\n- line 60: z\n- line 70: w\n')
    assert '2 unmatched' in out and 'FAIL' in out and code == 1


def test_slack_zero_misses_a_near_line(tmp_path):
    code, out = score(tmp_path, '- line 11: x\n- line 21: y\n', '--slack', '0')
    assert 'MISSED  K1' in out and 'caught  K2' in out and code == 1


def test_prose_lines_are_not_findings(tmp_path):
    code, out = score(tmp_path, 'I read line 10 closely.\n- line 40: lamp\n- :21 word\n')
    assert '2 of 3 caught, 0 unmatched' in out and code == 0


def test_nested_items_are_one_finding_at_their_first_line(tmp_path):
    report = ('1. - line 10: the tide\n   - against: page.md line 7, "the tide at seven"\n'
              '2. - line 40: the lamp\n   - against: page.md line 3\n')
    code, out = score(tmp_path, report)
    assert '2 of 3 caught, 0 unmatched' in out and code == 0


def test_must_column_refuses_a_finding_on_something_else(tmp_path):
    key = ("**Pass:** 1 of 1 caught.\n\n| ID | Line | Kind | Plant | Must |\n|---|---|---|---|---|\n"
           "| K1 | 11 | time | Thursday earlier than Wednesday | `thursday\|earlier\|eight and fifty` |\n")
    write(tmp_path, {'k.md': key, 'r1.md': '1. - line 11: she cannot read the letter\n',
                     'r2.md': '1. - line 11: Thursday is earlier than Wednesday\n'})
    import subprocess, sys
    a = subprocess.run([sys.executable, str(SCORE), 'k.md', 'r1.md'], cwd=tmp_path, capture_output=True, text=True).stdout
    b = subprocess.run([sys.executable, str(SCORE), 'k.md', 'r2.md'], cwd=tmp_path, capture_output=True, text=True).stdout
    assert 'MISSED  K1' in a and '1 unmatched' in a and 'caught  K1' in b


def test_a_quote_catches_a_plant_when_the_cited_line_is_miscounted(tmp_path):
    chapter = '\n'.join(['line one'] * 9 + ['Agnes was counting the rings aloud as Wren worked.'] + ['other text here and there'] * 5)
    key = ("**Pass:** 1 of 1 caught.\n\n| ID | Line | Kind | Plant |\n|---|---|---|---|\n| K1 | 10 | habit | counting aloud |\n")
    write(tmp_path, {'chapter.md': chapter, 'k.md': key,
                     'r1.md': '1. - line 7: quote: "counting the rings aloud as Wren worked"\n',
                     'r2.md': '1. - line 12: quote: "other text here and there"\n'})
    import subprocess, sys
    a = subprocess.run([sys.executable, str(SCORE), 'k.md', 'r1.md'], cwd=tmp_path, capture_output=True, text=True).stdout
    b = subprocess.run([sys.executable, str(SCORE), 'k.md', 'r2.md'], cwd=tmp_path, capture_output=True, text=True).stdout
    assert 'caught  K1' in a and 'by quote' in a
    assert 'MISSED  K1' in b
