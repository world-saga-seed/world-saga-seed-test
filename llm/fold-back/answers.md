# Key: fold-back

*Never give this file to the model under test.* The run (see run.md) copies book/ to `runs/fold-back/book/` and puts this section's [prose.md](prose.md) and [notes.md](notes.md) in place of 00400's prose and notes; the outline is the book's own. The fold-back edits that copy's outline and notes. [score.py](score.py) checks everything below.

The test prose differs from the book's draft 2 in four places, each with a right handling:

| What the prose does | Against | The fold-back must |
|---|---|---|
| Agnes reads at "the lamp-room window", not the gallery bench (line 3) | the outline's *(Proposal.)* beat 1.2, "Agnes below on the gallery bench with the almanac" | **fold it**: the beat now says the window, marked "(Proposal, from the draft, [00400](../prose/00400-the-forty-minutes.md).)", and "gallery bench" is deleted (the batch kept the choice: paper.md) |
| the weed on "the second post" (lines 25, 27) | the outline's *(Settled R0302-07.)* "Agnes sends her to look at the weed on the third post"; the causeway card, "The weed on the third post shows how long the water has been off" | **not fold it**: the settled line stays; a **drift** item on the Next pass list quoting the second post |
| no apron wipe (line 21) | the outline's *(Settled R0302-06.)* "Agnes wipes her hands on her apron before she has touched anything." | a **beat** item on the Next pass list naming the apron; the settled line stays |
| "and I did not tell her that either." (line 29) | held by the batch (paper.md, Critics) | a **held** item on the Next pass list quoting it |

And one open item the draft answers: the notes' "Open and flags" asks skirt or apron; the prose has "I rubbed the whiting off my thumb onto my skirt" (line 29). The fold-back replaces the question with the answer, marked "(Answered by the draft, 00400; overturnable.)".

## Required

| ID | Check |
|---|---|
| R1 | the prose file is unchanged |
| R2 | `## Next pass` is the notes' last section |
| R3 | every backticked quote in the Next pass section resolves in the prose (kit `tools/quotes.py --backticks`), and there is at least one |
| R4 | a Next pass item holds "drift" and a backticked quote with "second post" |
| R5 | a Next pass item holds "beat" and "apron" |
| R6 | a Next pass item holds "held" and the quote `did not tell her that either` |
| R7 | an outline line holds "(Proposal, from the draft", "window" and a link to `../prose/00400-the-forty-minutes.md` |
| R8 | the outline no longer holds "gallery bench" |
| R9 | every "(Settled" line of the book's outline is still in the copy, word for word |
| R10 | the notes hold "(Answered by the draft" on a line with "skirt", and "skirt or her apron?" is gone |
| R11 | every list line added to the outline or notes carries a mark ("(Proposal", "(Answered", "(Settled", "(Aim" or "(Resolved") |
| R12 | no struck text (`~~`) in the outline or notes |
| R13 | the report exists and its first line is `# Fold-back, 00400` |

**Pass:** all thirteen.

Read by hand: that the folded window beat is one line and copies no prose; whether a length item was added (the notes give the pilot as a 500-word opening, so none is due); the report's questions to the writer (the second post: the plain option, fix the page to the card).

## Lines verified

```text
$ grep -n "lamp-room window\|second post\|She turned the page\|did not tell her\|onto my skirt" prose.md | cut -c1-60
3:The lens was cleaned on the first dry morning of the month
11:"Wednesday. High water, nine and twelve. And forty." She 
21:"Then I said it Monday." She turned the page. "Friday. Te
25:When the sun was over the chimney she sent me down the ca
27:The causeway was bare for about four hours at each low wa
29:I rubbed the whiting off my thumb onto my skirt and walke
```
