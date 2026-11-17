# Invention check

The invention check (kit: plan/workflows/drafting/prompts/invention-check.md; the kit names no model, so Sonnet) judges a drafter's Inventions log against the cards and against what a person of the time and place would have to hand. [inventions.md](inventions.md) holds nine rows citing lines in [chapter.md](chapter.md), 00400 with the inventions written in: five faults (a habit the card forbids, a holm column in the almanac that would kill the clue, a borrowed wristwatch, a fourth post, Agnes explaining the forty) and four controls that stand. Paste [run.md](run.md) into a fresh Sonnet session in the repo's top folder; never show it [answers.md](answers.md). The shared scorer matches each non-standing verdict by the chapter line its row cites.

Score a run: `python3 llm/score.py llm/invention-check/answers.md runs/invention-check/report.md`

Baseline: not yet run.
