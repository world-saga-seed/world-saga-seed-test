# Run: attribution

**Model:** Sonnet (the kit names none; Sonnet is the default).

**How to run:** start a fresh session in this repo's top folder with that model, paste the block below (every `KIT/` replaced by the kit's folder, `../world-saga-seed/` or `../story-kit/`), and let it write its output, `runs/attribution/report.md`. It must never see `llm/attribution/answers.md`. Then score it: `python3 llm/attribution/score.py runs/attribution/report.md`.

**Filled for this book:** `{FILE}` is [test.md](test.md), built by the kit's `tools/attribution.py` (seed 7) from 00400, the 00200 sample and [agnes.md](agnes.md), a second head invented for this test since the book has only Wren's. `{WHAT}`, `{PERSON}` and `{HEADS}` describe the book without naming the chapters. The last line is added so score.py can read each paragraph's head.

```text
You are a cold reader for a test of a novel's prose, in the folder book/ (every path below is given from the repo's top folder). Read only one
file: llm/attribution/test.md. Read nothing else. Write only runs/attribution/report.md. Run no git commands and launch no agents.

The file holds paragraphs taken out of order from two chapters of The Tide Clock, a short novel set about 1890 on a northern coast, at a lighthouse on a tidal island, told in the first person, past tense, from inside the
heads of these people: 
- Wren Ashby, thirteen, apprenticed to the keeper since the autumn;
- Agnes Rook, in her sixties, keeper of the light for thirty-one years.
, one line each on who they are. Each paragraph is from inside
one head.

For each paragraph, say whose head it is in, how sure you are (sure, likely, guess), and in
one sentence what in the prose itself told you: the diction, the rhythm, what the
narration notices or cares about. Do not rely on who is named in it; say whether you could
tell from the voice alone. Then, in a short paragraph, say how distinct the voices are
overall, and name any paragraph whose voice seemed wrong for its head or could belong to
either.

Give each paragraph as a list item that begins `- P<n>: <name>,` with the head's first name (Wren or Agnes), or `either`, then how sure and why.
```
