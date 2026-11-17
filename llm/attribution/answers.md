# Key: attribution

*Never give this file to the model under test.* The kit's own key form, written by `tools/attribution.py` (seed 7) from three files: book/story/prose/00400-the-forty-minutes.md and book/story/voice/samples/sample-pages.md (Wren, the book's one head) and [agnes.md](agnes.md) (a second head invented for this test, Agnes, lines 5 to 17). The reader is given only [test.md](test.md).

- P1: 00400-the-forty-minutes.md:7, Wren
- P2: 00400-the-forty-minutes.md:17, Wren
- P3: agnes.md:11, Agnes
- P4: agnes.md:15, Agnes
- P5: agnes.md:9, Agnes
- P6: 00400-the-forty-minutes.md:23, Wren
- P7: 00400-the-forty-minutes.md:3, Wren
- P8: sample-pages.md:3, Wren
- P9: 00400-the-forty-minutes.md:27, Wren
- P10: agnes.md:13, Agnes
- P11: agnes.md:5, Agnes
- P12: sample-pages.md:13, Wren
- P13: agnes.md:17, Agnes
- P14: agnes.md:7, Agnes
- P15: sample-pages.md:15, Wren

**Planted:** P4 (agnes.md:15). Agnes's head (her own eyes on the almanac print, her own apron), written in Wren's voice: short words, comparisons from home and the village (a mother threading a needle at the window, minnows at the slip), the hands. Caught when the reader gives it to Wren, calls it "either", or names it in the closing paragraph as wrong for its head.

**Pass:** 13 of 14 clean paragraphs to the right head, P4 caught, at most 1 false flag (a clean paragraph called "either" or named as wrong for its head).

Score with `python3 llm/attribution/score.py REPORT`.
