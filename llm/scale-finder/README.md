# Scale finder

The scale finder (kit: plan/workflows/drafting/prompts/scale-finder.md, Haiku) lists every line that states or implies a size, a height, a reach or a fit, for the facts critic to judge; it does not judge. The book has no heights table, so the heights (Wren 150 cm, Agnes 152 cm) and [size-facts.txt](size-facts.txt) are invented here, and the prompt's sheet head is tools/scale.py's. Three size lines are planted in [chapter.md](chapter.md) (Agnes a head taller, her feet clear of the floor, the rail at her chin), each wrong against those numbers, and the key also holds the chapter's two original size lines (the step stool, the hand's width), since a finder is scored on finding all of them. It reads only the chapter. Paste [run.md](run.md) into a fresh Haiku session in the repo's top folder; never show it [answers.md](answers.md).

Score a run: `python3 llm/score.py llm/scale-finder/answers.md runs/scale-finder/report.md`.

Baseline: not yet run.
