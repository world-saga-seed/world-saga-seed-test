# Drafter

The drafter (kit: plan/workflows/drafting/prompts/drafter.md; the kit names no model, so Sonnet) drafts a chapter from its outline, notes, voice files and cards. This section drafts 00700, Caught on the causeway, which has an outline (two settled beats and the writer's missing frame) and no prose; [knowledge-00700.md](knowledge-00700.md) is the kit's tools/knowledge.py on Wren's guard. Paste [run.md](run.md) into a fresh Sonnet session in the repo's top folder and save its final report to runs/drafter/report.md; never show it [answers.md](answers.md). [score.py](score.py) checks each beat's must-have words, 0 banned-word hits and the texture bands with the kit's tools/tells.py, the title line, and that the report leaves Agnes's answer open; a hand-made 140-word draft with both beats passes, and the same draft with "I realized", "sandbar" and the third post dropped fails three checks. What the script cannot read (Agnes never explaining, the brief's end state) is listed in the key for a reader.

Score a run: `python3 llm/drafter/score.py runs/drafter/00700-caught-on-the-causeway.md --report runs/drafter/report.md`

Baseline: not yet run.
