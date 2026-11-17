"""cards.py integrity: what an agent must be able to trust on a card, failing only on finished cards."""
from conftest import run, write

FORMS = 'world/beast\tBody; Threat; Name; Appears in; Open?\n'
LEDGER = '| ID | Ruling |\n|---|---|\n| R0302-01 | Selkies are grey. |\n'


def card(name, body, head_extra=''):
    return f'# {name}: a beast\n\n*Summary.*\n\nKeywords: sea\n\n{head_extra}## {name}\n\n{body}'


def book(tmp_path, cards):
    files = {'forms.tsv': FORMS, 'plan/ledger/2027-03-02.md': LEDGER,
             'world/beast/README.md': '# Beasts\n',
             'story/prose/00400-the-forty-minutes.md': '# 00400\n\nA selkie in the harbour.\n',
             'story/prose/00500-the-inspector.md': '# 00500\n\nNo beasts here.\n'}
    files.update({f'world/beast/{k}.md': v for k, v in cards.items()})
    return write(tmp_path, files)


GOOD = ('- **Body.** *(Settled, R0302-01.)* Grey.\n- **Threat.** *(Settled, R0302-01.)* Low.\n'
        '- **Name.** Selkie.\n- **Appears in.** 00400.\n')


def args():
    return ('cards', 'integrity', '--forms', 'forms.tsv', '--ledger', 'plan/ledger', '--prose', 'story/prose')


def test_a_finished_card_in_good_order_passes(tmp_path):
    book(tmp_path, {'selkie': card('Selkie', GOOD, '*(Distilled from abc1234.)*\n\n')})
    code, out = run(*args(), cwd=tmp_path)
    assert code == 0, out
    assert out.strip().splitlines()[-1].startswith('1 cards, 1 finished; problems: 0')


def test_a_proposal_or_an_unmarked_field_fails_a_finished_card(tmp_path):
    body = GOOD.replace('*(Settled, R0302-01.)* Low.', '*(Proposal.)* Low.').replace('*(Settled, R0302-01.)* Grey.', 'Grey.')
    book(tmp_path, {'selkie': card('Selkie', body, '*(Distilled from abc1234.)*\n\n')})
    code, out = run(*args(), cwd=tmp_path)
    assert code == 1
    assert 'PROBLEM: proposal left on a finished card' in out
    assert 'PROBLEM: field with no status mark: Body' in out
    assert 'no status mark: Name' not in out and 'no status mark: Appears in' not in out


def test_the_same_faults_on_an_unfinished_card_are_listed_not_failed(tmp_path):
    body = GOOD.replace('*(Settled, R0302-01.)* Low.', '*(Proposal.)* Low.')
    book(tmp_path, {'selkie': card('Selkie', body)})
    code, out = run(*args(), cwd=tmp_path)
    assert code == 0 and 'proposal left' not in out                 # proposals are only a fault once finished


def test_a_ruling_the_ledger_lacks_a_broken_link_and_a_task_cited(tmp_path):
    body = GOOD.replace('R0302-01.)* Low', 'R0302-09.)* Low') + \
        '- **Open.** See [the inspector](../../story/outline/00500-x.md), [gone](#nowhere), [the task](../../plan/tasks/task-20270302-01-x.md).\n'
    book(tmp_path, {'selkie': card('Selkie', body, '*(Finished.)*\n\n')})
    write(tmp_path, {'plan/tasks/task-20270302-01-x.md': '# T\n'})
    code, out = run(*args(), cwd=tmp_path)
    assert 'ruling not in the ledger: R0302-09' in out
    assert 'link to no file: ../../story/outline/00500-x.md' in out
    assert 'link to no heading: #nowhere' in out
    assert 'a task cited: ../../plan/tasks/task-20270302-01-x.md' in out


def test_missing_and_misordered_fields(tmp_path):
    body = '- **Threat.** *(Settled.)* Low.\n- **Body.** *(Settled.)* Grey.\n- **Name.** Selkie.\n'
    book(tmp_path, {'selkie': card('Selkie', body, '*(Finished.)*\n\n')})
    code, out = run(*args(), cwd=tmp_path)
    assert 'missing field: Appears in' in out and 'fields out of order' in out and 'missing field: Open' not in out


def test_appears_in_checked_against_the_prose_both_ways_by_the_name_field(tmp_path):
    body = GOOD.replace('- **Name.** Selkie.', '- **Name.** *selkie*, from the old word.').replace('00400.', '00500.')
    book(tmp_path, {'selkie': card('Grey seal of the holm', body)})
    code, out = run(*args(), cwd=tmp_path)
    assert 'check: Appears in lists 00500, whose prose never names "selkie"' in out
    assert 'check: 00400 names "selkie" but Appears in does not list it' in out


def test_a_long_run_shared_by_two_cards_is_listed(tmp_path):
    same = 'the tide comes in over the bar forty minutes after the almanac says it will every day'
    book(tmp_path, {'selkie': card('Selkie', GOOD + f'\n{same}.\n'), 'gull': card('Gull', f'- **Body.** {same}.\n')})
    code, out = run(*args(), '--shared', '12', cwd=tmp_path)
    assert 'world/beast/gull.md: check: shares "' in out and 'with world/beast/selkie.md' in out
