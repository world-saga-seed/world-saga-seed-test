# Key: drafter

*Never give this file to the model under test.* The chapter is 00700, Caught on the causeway: its outline (book/story/outline/00700-caught-on-the-causeway.md) has two settled beats and one missing frame, and no prose exists. Everything below is checked by [score.py](score.py), which reads this file.

## Beats

Each beat's must-have words: every pattern must appear in the draft (a regular expression, case ignored; "|" separates alternatives).

| Beat | Outline line | Must hold |
|---|---|---|
| 1 | The inspector sets out from Saltby by the printed table. | `inspector\|Board's man` ; `Saltby` ; `table\|almanac` |
| 2 | Wren, coming back from the village, remembers "and forty" and waits at the third post. | `and forty` ; `third post` ; `wait` |
| 3 | *(Missing: the writer's frame.)* What Agnes says when Wren asks her about "and forty". | none on the page; the report must list it as left open (see Report) |

## Banned

book/story/voice/banned.txt, run by the kit's `tools/tells.py --banned`: **0 hits** in narration. The list holds "sandbar" and "tidal lag": the page never says why the water runs late (K3, book/story/voice/pov.md).

## Texture

The voice sheet (book/story/voice/voice.md, Texture) gives one number per measure, from the writer's sample; this key sets the band around it. The bands hold both the sample (and/s 0.94, way/k 0.0, sd 12.2) and the refined 00400 (0.49, 0.0, 9.9), so a draft in the book's voice passes.

| Measure | Low | High |
|---|---|---|
| and/s | 0.40 | 1.30 |
| way/k | 0.0 | 1.0 |
| sd | 8.0 | 16.0 |

## Title

The first line is exactly `# Caught on the Causeway (draft 1)`.

## Report

When the drafter's report is given (`--report`), it must hold an Inventions list (a line with "Inventions") and a line that leaves Agnes's answer open (a line holding "open" and "Agnes" or "forty").

## Read by hand

The script cannot check these; read the draft for them: no line in which Agnes explains the forty (the writer dictates it); Wren's knowledge at 00700 (llm/drafter/knowledge-00700.md: she knows Agnes's eyes, believes the table is the holm's until the crossing); the inspector safe and Agnes's secret held, as the brief's end state asks; nothing Dell does beyond the brief's proposal.

**Pass:** every beat pattern, 0 banned hits, all three measures in band, the title line; and, with `--report`, the report checks.
