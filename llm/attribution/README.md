# Attribution test

The attribution test (kit: plan/workflows/drafting/prompts/attribution.md; the kit names no model, so Sonnet) gives a cold reader unlabeled paragraphs and asks whose head each is in, by voice alone. The Tide Clock has one head, so [agnes.md](agnes.md) adds a second, Agnes, for this test only; [test.md](test.md) is the kit's tools/attribution.py output on 00400, the 00200 sample and agnes.md: eight paragraphs of Wren, seven of Agnes, one of them (P4) Agnes's head written in Wren's voice, the kit's calibration plant. [answers.md](answers.md) is the kit's key form with the plant marked. Paste [run.md](run.md) into a fresh Sonnet session in the repo's top folder; never show it answers.md or agnes.md. [score.py](score.py) checks each paragraph's head, the plant and false flags; on a hand-made report with every head right and P4 named wrong for its head it passes, and with P4 missed and one clean paragraph called "either" it fails.

Score a run: `python3 llm/attribution/score.py runs/attribution/report.md`

Baseline: not yet run.
