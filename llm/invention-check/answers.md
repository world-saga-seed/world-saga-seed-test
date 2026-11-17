# Key: invention check

*Never give this file to the model under test.* The input is [inventions.md](inventions.md), nine rows from a drafter's Inventions list, each citing its line in [chapter.md](chapter.md) (00400 of *The Tide Clock*, draft 2, with the planted inventions written in and a short invented noon added after line 29). Five rows are faults; four stand. The key's lines are the **chapter lines** the rows cite, so a finding names the line its row cites.

| ID | Line | Kind | Plant |
|---|---|---|---|
| K1 | 5 | break | row 1, Agnes counts the rings aloud. Card: "**Not:** she never counts aloud, and never explains a habit." (book/world/people/agnes-rook.md, Habits) |
| K2 | 17 | break | row 2, the almanac prints a column for the holm. Card: "Nobody prints a table for the holm." (book/world/places/the-causeway.md, Why the water runs late); the tide table card has it right for the harbor only, and the clue dies if the table is right |
| K3 | 25 | reword | row 4, a wristwatch Dell lent her. Not a card clash; what is to hand fails: a lighthouse of 1890 keeps a clock for the log's times (row 9), and a village girl would not be lent a watch. Fix: tell the hour by the lamp-room clock, or by the sun over the chimney, as draft 2 does |
| K4 | 31 | break | row 6, a fourth post. Card: "Three tarred posts mark the way." (book/world/places/the-causeway.md, The posts; R0302-07) |
| K5 | 37 | break, or to the writer | row 8, Agnes explains the forty by the bar. Card: "she never counts aloud, and never explains a habit"; "This is author-side: the page never explains it" (the causeway, Why the water runs late); and what she says when asked is the writer's open frame, "the writer dictates it, 00700" (agnes-rook.md, Open) |

**Pass:** 3 of 5 caught, at most 2 unmatched.

A catch is any verdict but "stands" on the row; break against reword is read by hand, not scored. "To the writer" on K5 is as right as "break".

## Rows that stand

A finding on these is unmatched. They are the controls: consistent, and ordinary for the place and time.

| Row | Line | Why it stands |
|---|---|---|
| 3 | 23 | a curved glass shows the room upside down; the worked run's invention check passed it (book/reports/revision-00400.md, Re-check 6) |
| 5 | 27 | green weed where the water lies longest; nothing on the causeway card says otherwise |
| 7 | 35 | an old way of cutting a loaf in a house without a board; touches nothing |
| 9 | 41 | the log records "the time the lamp was lit and put out" (book/world/things/the-log-book.md), so the house keeps a clock |

## Lines verified

```text
$ grep -n "counted them off\|second column\|upside down\|wristwatch\|green to the second\|fourth at\|cut the bread\|bar off the holm\|clock struck" chapter.md | cut -c1-50
5:"Ring by ring," she said, and she counted them o
17:I minded it. The almanac was printed in Saltby 
23:My grandmother had done the same at the end. Sh
25:When the wristwatch Dell had lent me said half 
27:The causeway was bare for about four hours at e
31:On the way back I counted the posts, as Dell ha
35:We ate at noon at the table under the stair. Mr
37:"You asked me about the forty," she said, when 
41:At four the lamp-room clock struck, and she sen
```
