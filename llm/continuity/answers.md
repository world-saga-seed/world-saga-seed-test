# Key: continuity critic

*Never give this file to the model under test.* The input is [chapter.md](chapter.md): 00400 of *The Tide Clock* (draft 2) with four seams broken, against the chapter's own other lines and against the page before it, the oil-cart scene (book/story/voice/samples/sample-pages.md). Nothing else is changed.

**Pass:** 3 of 4 caught, at most 2 unmatched.

| ID | Line | Kind | Plant | Must |
|---|---|---|---|---|
| K1 | 11 | times that do not add up | Thursday's high water read as "eight and fifty-one", earlier than Wednesday's "nine and twelve" on the same line, while Friday's is "Ten and thirty" (line 21): the times go back a day and then forward. The original is "nine and fifty-one" (book/story/prose/00400-the-forty-minutes.md, line 11) | `thursday\|earlier\|eight and fifty\|go(es)? back\|out of order` |
| K2 | 17 | name changed | the almanac "printed in Saltburn": the page before has "the schoolmaster in Saltby" (book/story/voice/samples/sample-pages.md, line 15), and the village is Saltby throughout the book | `saltburn` |
| K3 | 23 | sentence reused | "holding the almanac at arm's length and then close and then at arm's length again", reused from the oil cart: "She held it at arm's length and then close and then at arm's length again." (book/story/voice/samples/sample-pages.md, line 7). The original reads "bent over the almanac" | `arm's length\|reused\|repeat` |
| K4 | 29 | beat told twice | "By the almanac, low water had been an hour ago" said again, two lines after line 27 says it word for word | `twice\|again\|repeat` |

## Real faults already in the chapter

- None.
