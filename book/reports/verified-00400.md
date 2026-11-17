# Verified findings, 00400 (the batch paper's merged list)

*The supervisor's merge of [the facts critic](critic-facts-00400.md) and [the voice critic](critic-voice-00400.md), in text order, after verification. Checked against draft 1 ([snapshot](snapshot/00400-the-forty-minutes.md)).*

## Verification

```text
$ python3 tools/quotes.py example/reports/critic-facts-00400.md --in example/reports/snapshot/00400-the-forty-minutes.md
MISSING  example/reports/critic-facts-00400.md:22  the lens was cleaned every Sunday
2 of 3 quotes resolve
$ python3 tools/quotes.py example/reports/critic-voice-00400.md --in example/reports/snapshot/00400-the-forty-minutes.md
4 of 4 quotes resolve
```

- **Dropped, quote missing:** facts 3 ("the lens was cleaned every Sunday"). Counted against the facts critic.
- **Rules exist:** every cited heading is in the voice sheet or the card cited.
- **Not the writer's lines:** no quote is in [the sample](../story/voice/samples/sample-pages.md).
- **Clues:** voice 1 touches a clue line listed in [the chapter's notes](../story/notes/00400-the-forty-minutes.md): "By the almanac, low water had been an hour ago." Its direction is changed: the clue stays.

## The list

| # | Line | Critic | Finding | Severity | Disposition |
|---|---|---|---|---|---|
| 1 | 17 | facts 2 | "the only book in the house besides the log and the Bible" against the Board's Instructions on the shelf | weak | **Keep.** Wren would not count the Board's book as the house's; it is her voice. *(Resolved by judgment, overturnable.)* |
| 2 | 23 | voice 2 | the lens told as a tally | weak | **Fix.** One ring seen close in place of the tally. To the reviser. |
| 3 | 27 | facts 1 | two hours against the card's four | break | **Fix now.** "about four hours at each low water" (R0302-07). |
| 4 | 27 | voice 4 | "which meant the water had only just gone off it" | weak | **Dropped on a fair reading.** Wren learned the weed line from Dell in 00300; this is what she knows, not the narration explaining the tide. The tide's cause (the sandbar) stays off the page. |
| 5 | 27 | voice 1 | the clue lined up for the reader | weak | **Fix, in part.** Keep the clue sentence word for word; cut the echo "By the weed, it had been no time at all." To the reviser. |
| 6 | 29 | voice 3 | the closing line repeats the beat | taste | **Keep.** The withholding is the chapter's point, and the writer's sample ends a scene the same way. Logged. |

## To the reviser

- Finding 2: trade "I finished the sixth ring and the seventh, and changed the water, and started on the bull's-eye in the middle" for one ring seen close. No new fact.
- Finding 5: cut "By the weed, it had been no time at all." Keep "By the almanac, low water had been an hour ago." exactly.

## Keep list

In [keep-00400.md](keep-00400.md): the clue lines and the habit line, which the revision must leave word for word.

## To the writer

- None from this chapter. Finding 1's judgment is listed for an overturn if the writer wants the Instructions named.
