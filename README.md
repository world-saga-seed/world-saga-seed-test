# world-saga-seed-test

Tests for [world-saga-seed](https://github.com/world-saga-seed/world-saga-seed), the kit for writing a long novel with Claude. One section for each piece of the kit, so you can check any of them yourself before you trust it with your book.

There are two kinds of tests:

- **`python/`, the tools.** Each kit script has a section of planted cases: a small fixture with a known answer, and a near miss that must not be flagged. They cost nothing to run and finish in seconds.
- **`llm/`, the prompts.** Each critic, finder and judge prompt has a chapter with faults planted in it, an answer key, and a scorer that counts what the prompt caught, missed and invented. They spend tokens, and each section states its cost before you run it.

Every test runs on **`book/`**: *The Tide Clock*, an invented novel (copied from the kit's `example/`). It belongs to no real book, so these tests can be public.

## Run the tool tests

You need Python 3.9 or newer, pytest, and a copy of the kit beside this repo (`../world-saga-seed`). If the kit is somewhere else, set `WSS_KIT` to its folder.

```bash
python3 -m pip install pytest
python3 -m pytest -q                     # every tool
python3 -m pytest -q python/test_stutters.py   # one tool
```

**A pass** means the tool does what its docstring promises on every planted case. **An xfail** is a known bug in the kit, written down with the fixture that shows it. It turns into a failure once the bug is fixed, as a reminder to remove the mark. **A failure** is a regression: send the failing case with your report.

Many cases come from bugs found by running a tool on a real book. Each such case is named for what it plants: a link to a sibling outline that shares a retired draft's file name, a ruling ID read short, a sound span counted as earlier in its own chapter.

## Run the prompt tests

Each section in `llm/<prompt>/` holds:

- `chapter.md`, a test chapter with faults planted in it;
- `answers.md`, the answer key: each planted fault, where it is and what kind;
- `run.md`, the prompt with its fields filled in, to paste or launch;
- `score.py`, which reads the prompt's report and prints caught, missed and invented;
- `baseline.md`, one recorded run: the model, the date, the score and the tokens.

A prompt passes when it catches the key's plants without inventing faults. Compare your model's score with the baseline.

## Baselines

One cold run of each prompt, 2026-11-17, each by the model the kit names; each section's `baseline.md` says what the unmatched findings were, read one by one. About 845,000 tokens for the eighteen.

| Prompt | Model | Score | Result |
|---|---|---|---|
| [facts](llm/facts/baseline.md) | Sonnet | 5 of 5 | PASS |
| [continuity](llm/continuity/baseline.md) | Sonnet | 3 of 4 | PASS |
| [coverage-slip](llm/coverage-slip/baseline.md) | Sonnet | 5 of 5 | PASS |
| [setup-belief](llm/setup-belief/baseline.md) | Sonnet | 4 of 4 | PASS |
| [voice-mechanism](llm/voice-mechanism/baseline.md) | Sonnet | 5 of 5 | PASS |
| [habits](llm/habits/baseline.md) | Sonnet | 5 of 5 | PASS |
| [idioms](llm/idioms/baseline.md) | Sonnet | 5 of 5 | PASS |
| [procedures](llm/procedures/baseline.md) | Sonnet | 4 of 4 | PASS |
| [scale-finder](llm/scale-finder/baseline.md) | Haiku | 5 of 5 | PASS |
| [inference-finder](llm/inference-finder/baseline.md) | Haiku | 5 of 5, near misses listed as ungrounded | FAIL (the judge clears them) |
| [inference-judge](llm/inference-judge/baseline.md) | Sonnet | 4 of 5, no near-miss errors | PASS |
| [invention-check](llm/invention-check/baseline.md) | Sonnet | 5 of 5 | PASS |
| [outline-critic](llm/outline-critic/baseline.md) | Sonnet | 5 of 5 | PASS |
| [attribution](llm/attribution/baseline.md) | Sonnet | 14 of 14 clean, plant missed | FAIL |
| [librarian](llm/librarian/baseline.md) | Haiku | 8 of 8 | PASS |
| [drafter](llm/drafter/baseline.md) | Sonnet | all mechanical checks | PASS |
| [reviser](llm/reviser/baseline.md) | Sonnet | 4 of 4 fixed, 4 of 4 kept | PASS |
| [fold-back](llm/fold-back/baseline.md) | Sonnet | 13 of 13 | PASS |

Run a prompt with `python3 llm/brief.py <section>`: it prints the block with the one rule a cold run adds (never open a section's `answers.md`), and fills in the kit's folder where the prompt runs kit tools. A run's own safety check should also keep it out of `llm/*/answers.md`; one baseline tried to open its key first and was refused.

## Add a case

Found a tool or prompt getting something wrong on your own book? Make the smallest invented fixture that shows it, with none of your book's text, and add it to that section. Mark it `xfail` with the reason until the kit is fixed.

## License

As the kit.
