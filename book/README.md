# The example: one small novel through every stage

This folder is a writer's repo in miniature. It carries one invented premise through the whole method, so each stage has something real to point at. Nothing here is a real book.

## The premise

*The Tide Clock* (working title). Around 1890, on a northern coast. Wren Ashby, thirteen, is apprenticed to Agnes Rook, the keeper of the light on Skerry Holm, a tidal island joined to the village of Saltby by a stone causeway that floods twice a day. Agnes's eyes are failing, and she hides it, because the Lighthouse Board would retire her. Wren thinks Agnes's mind is going too, because she adds "and forty" to every tide she reads aloud. It is not her mind. The printed tide table is for Saltby harbor, and the island's water runs about forty minutes later. When the Board's inspector comes at the spring tides and trusts the printed table, Agnes's habit is what saves him, and Wren's eyes are what keep Agnes in her post.

It is small on purpose: four people, three places, one secret, one clue.

## The stages, and where each one shows here

| Stage | What it made | File |
|---|---|---|
| 01 Intake | A look at the writer's existing pages, picked in the interview as the style sample and copied by stage 03 (the example keeps only the copy) | [story/voice/samples/sample-pages.md](story/voice/samples/sample-pages.md) |
| 02 Interview | The answers, each with where it landed | [interview-record.md](interview-record.md) |
| 03 Set up plan/ | The chapter state table | [plan/state.md](plan/state.md) |
| 04 Card the work | Four cards and a character sheet | [world/](world/README.md), [story/notes/characters/wren.md](story/notes/characters/wren.md) |
| 04 Card the work | The rulings of one session | [plan/settled/ledger/2027-03-02.md](plan/settled/ledger/2027-03-02.md) |
| 06 Outline | The arc outline and one chapter outline | [story/outline/1-spring-tides.md](story/outline/1-spring-tides.md), [story/outline/00400-the-forty-minutes.md](story/outline/00400-the-forty-minutes.md) |
| 07 Key frames | The writer's frames and Claude's tweens, and one brief | [story/notes/1-spring-tides-key-frames.md](story/notes/1-spring-tides-key-frames.md) |
| 08 Notes, then render | The voice sheet, the banned list, one drafted scene | [story/voice/voice.md](story/voice/voice.md), [story/voice/banned.txt](story/voice/banned.txt), [story/prose/00400-the-forty-minutes.md](story/prose/00400-the-forty-minutes.md) |
| 09 Refine | The worked run: two critic reports on draft 1, the verified list, the keep list, the revision and re-check | [critic-facts](reports/critic-facts-00400.md), [critic-voice](reports/critic-voice-00400.md), [verified](reports/verified-00400.md), [keep](reports/keep-00400.md), [revision](reports/revision-00400.md); draft 1 in [reports/snapshot/](reports/snapshot/00400-the-forty-minutes.md) |
| 06 and 10 Reader tests | The spec (a six-entry key, three story questions) and a mock blind probe with one leak and one miss | [plan/reader-tests/key.md](plan/reader-tests/key.md), [plan/reader-tests/questions.md](plan/reader-tests/questions.md), [reports/probe-00100-00400.md](reports/probe-00100-00400.md) |
| 10 Read | A mock interest table, with a lull that sets up a payoff | [reports/interest-merged.md](reports/interest-merged.md) |

## Try the tools on it

From the kit's top folder:

```bash
python3 tools/links.py --root example
python3 tools/cards.py check --root example/world
python3 tools/tells.py example/story/prose/*.md example/story/voice/samples/sample-pages.md --banned example/story/voice/banned.txt
python3 tools/repeats.py example/story/voice/samples/sample-pages.md example/story/prose/*.md --min-files 2
python3 tools/quotes.py example/reports/critic-facts-00400.md --in example/reports/snapshot/00400-the-forty-minutes.md
python3 tools/quotes.py example/reports/keep-00400.md --in example/story/prose/00400-the-forty-minutes.md
python3 tools/epub.py --title "The Tide Clock: Spring Tides" --author "A. Writer" --out build/tide-clock.epub \
    --prose example/story/prose --outline example/story/outline --from 100 --to 800
```

The first quotes check is meant to report one missing quote: the facts critic made a finding whose quote is not in draft 1, and the verified list shows it dropped. That is the check working. The second confirms the revision kept every clue line.
