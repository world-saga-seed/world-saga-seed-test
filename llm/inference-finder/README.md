# Inference finder

The inference finder (kit: plan/workflows/drafting/prompts/inference-finder.md, Haiku) lists every line where a first-person narrator states what she could only infer, each paired with its evidence or "none on the page". [chapter.md](chapter.md) is 00400 with an invented afternoon added and five ungrounded claims planted (another's feeling, a motive, a carter's past, another's thought, a cause from before Wren was born), plus two near misses grounded a line earlier, which it must list with their evidence, not as "none on the page". A finder lists widely, so findings off the plants are not capped. Paste [run.md](run.md) into a fresh Haiku session in the repo's top folder; never show it [answers.md](answers.md). The section's [score.py](score.py) runs llm/score.py and adds the near-miss check.

Score a run: `python3 llm/inference-finder/score.py runs/inference-finder/finds.md`

Baseline: not yet run.
