# Key: outline critic

*Never give this file to the model under test.* The input is [outline.md](outline.md), a copy of book/story/outline/00400-the-forty-minutes.md with five faults planted: three beats changed, two sections added (5 and 6). Every other line is the book's own.

| ID | Line | Kind | Plant |
|---|---|---|---|
| K1 | 10 | contradiction | Agnes "counting the rings aloud". Card: "**Not:** she never counts aloud, and never explains a habit." (book/world/people/agnes-rook.md, Habits; R0302-06) |
| K2 | 19 | contradiction | Agnes "gives in and tells her the holm's water runs forty minutes behind". Against the settled beat three lines up, "Agnes says to mind her ring. No explanation." (line 16, R0302-06); the card's "never explains a habit"; the causeway card, "the page never explains it"; and the open frame, "what she says when Wren asks about "and forty" (the writer dictates it, 00700)" (agnes-rook.md, Open) |
| K3 | 28 | contradiction | "bare for only an hour at low water". Card: "It is bare for about four hours at each low water" (book/world/places/the-causeway.md, What it is; R0302-07) |
| K4 | 34 | cause | Dell's cart arrives "just as she turns back" and he explains the posts: help on cue, with no cause (Dell comes with the oil, the tide table card has him bring the almanac each January, and nothing brings him this morning); and the notes' "Cast on the page: Wren, Agnes." (book/story/notes/00400-the-forty-minutes.md, Notes for drafting) |
| K5 | 40 | contradiction | Wren "works out ... that the printed table is wrong for the holm" this evening. Against the Aim at line 30, "The reader puts the two together before Wren does"; the sheet's arc, "At the crossing, joins the weed and "and forty", and waits." (book/story/notes/characters/wren.md, Her arc 3); the knowledge guard's Believes 2 (from 00100; turns at 00700) |

**Pass:** 3 of 5 caught, at most 2 unmatched.

Kind and severity are read by hand, not scored. All five are breaks except K4, which a critic may fairly call weak.

## Lines verified

```text
$ grep -n "counting the rings\|gives in\|only an hour\|oil cart comes\|works out from" outline.md | cut -c1-60
10:- *(Proposal.)* Wren on the step stool inside the lamp, w
19:- *(Proposal.)* Pressed a second time, Agnes gives in and
28:- *(Proposal.)* The causeway is bare for only an hour at 
34:- *(Proposal.)* Dell's oil cart comes over the causeway j
40:- *(Proposal.)* That evening Wren works out from the weed
```
