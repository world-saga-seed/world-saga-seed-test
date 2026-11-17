# Revision and re-check, 00400

*The reviser's work on [the verified list](verified-00400.md), from the snapshot of draft 1, and the supervisor's re-check. The chapter is now [draft 2](../story/prose/00400-the-forty-minutes.md).*

## The revised paragraphs

**Finding 2, the lens (line 23).**

> Before: So I said nothing more about it. I finished the sixth ring and the seventh, and changed the water, and started on the bull's-eye in the middle, which was the hardest, because it showed every smear.

> After: So I said nothing more about it. I took the leather to the last ring before the middle. The whiting dried white in the cuts of the glass, and when I rubbed it off, the ring threw the window back at me upside down, small and bright, with Mrs. Rook in it, bent over the almanac. Then I changed the water and started on the bull's-eye, which was the hardest, because it showed every smear.

**Findings 3 and 5, the causeway (line 27).**

> Before: The causeway was bare for two hours at every low water, never more, and you learned to walk it fast. … By the almanac, low water had been an hour ago. By the weed, it had been no time at all.

> After: The causeway was bare for about four hours at each low water, and you learned to walk it fast anyway. … By the almanac, low water had been an hour ago.

## The reviser's report

| # | Finding | Done |
|---|---|---|
| 2 | the lens as a tally | the tally cut; one ring seen close, its reflection of the room. The "and" chain is gone. |
| 3 | four hours (fixed by the supervisor first) | left as fixed |
| 5 | the clue lined up | the echo cut; the clue sentence kept exactly |

**Inventions:** one. The lens ring shows the room reflected upside down (line 23). Touches: nothing carded; a fact of lenses. Sent to the invention check.

## Re-check

```text
$ python3 tools/tells.py example/reports/snapshot/00400-the-forty-minutes.md example/story/prose/00400-the-forty-minutes.md --banned example/story/voice/banned.txt
00400-the-forty-minutes.md     w=  455 way/k= 0.0 asif/k= 0.0 and/s=0.51 ...   (draft 1)
00400-the-forty-minutes.md     w=  484 way/k= 0.0 asif/k= 0.0 and/s=0.49 ...   (draft 2)
0 banned-word hits
$ python3 tools/quotes.py example/reports/keep-00400.md --in example/story/prose/00400-the-forty-minutes.md
6 of 6 quotes resolve
```

1. **Diff against the snapshot:** three changes, each tied to a finding. No stray edits.
2. **Keep list:** 6 of 6 on the page.
3. **Mechanical checks:** no banned word; texture inside the sample's range (and/s fell a little, as the chain was broken; not chopped).
4. **The fix, not only the finding:** finding 2's fault was that the work did not hold Wren. The new lines give the work and put Agnes in it; fixed. Finding 5's fault was the paired comparison; the reader is still given both halves (the almanac line here, the weed above), but not the conclusion; fixed.
5. **Facts over the changed passages:** "about four hours" matches the card; the lens reflecting the room breaks nothing. No findings.
6. **Invention check:** the reflection stands (an ordinary property of a curved glass a girl cleaning one would see).

Stage of 00400 in [plan/state.md](../plan/state.md): **refined**. The drift row for the causeway's hours is deleted: the page now matches the card.
