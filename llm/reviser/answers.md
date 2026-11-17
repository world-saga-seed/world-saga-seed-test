# Key: reviser

*Never give this file to the model under test.* The input is [chapter.md](chapter.md), 00400 of *The Tide Clock* (draft 2) with four faults written back in, the findings that name them, [findings.md](findings.md), and the keep list, [keep.md](keep.md). Finding 4 sits on the same line as a clue the keep list holds: the reviser must cut the echo and keep the clue.

## Gone

Each fault's text must be gone from the revised file (spacing, curly quotes and emphasis ignored).

| ID | Line | Gone |
|---|---|---|
| F1 | 17 | `I did not know yet` |
| F2 | 23 | `I realized` |
| F3 | 27 | `two hours at every low water` |
| F4 | 27 | `By the weed, it had been no time at all` |

## Kept

Every quote in [keep.md](keep.md) still in the revised file, word for word (checked with the kit's `tools/quotes.py`):

- line 11: High water, nine and twelve. And forty.
- line 21: She wiped her hands on her apron, though she had not touched anything.
- line 27: The weed on the third post was still wet a hand's width above the mud
- line 27: By the almanac, low water had been an hour ago.

## Title

The first line unchanged: `# The Forty Minutes (draft 2)`

**Pass:** all four gone, all four kept, the title unchanged.

Read by hand: whether F2's fix still shows the whiting drying, and F3's says about four hours (the card), not some other number; whether any fact was added (the prompt allows none).

## Lines verified

```text
$ grep -n "did not know yet\|I realized\|two hours at every\|no time at all" chapter.md | cut -c1-50
17:I minded it. The almanac was printed in Saltby 
23:My grandmother had done the same at the end. Sh
27:The causeway was bare for two hours at every lo
$ grep -n "nine and twelve. And forty\|She wiped her hands\|a hand.s width\|By the almanac, low" chapter.md | cut -c1-50
11:"Wednesday. High water, nine and twelve. And fo
21:"Then I said it Monday." She wiped her hands on
27:The causeway was bare for two hours at every lo
```
