# Key: habits critic

*Never give this file to the model under test.* The input is [chapter.md](chapter.md): 00400 of *The Tide Clock* (draft 2) with five habit faults planted: two "Not:" habits shown, two habits swapped between the two people, and one habit explained. Nothing else is changed.

**Pass:** 3 of 5 caught, at most 2 unmatched.

| ID | Line | Kind | Plant |
|---|---|---|---|
| K1 | 5 | Not: habit shown, Agnes | Agnes "counted them aloud for me, one to nine": "**Not:** she never counts aloud" (book/world/people/agnes-rook.md, Habits); "she does not count things aloud (that is nobody's habit in this book)" (book/story/notes/characters/wren.md, Habits) |
| K2 | 11 | Not: habit explained, Agnes | Agnes adds "My husband read them so, and I keep it for him.": "**Not:** she never counts aloud, and never explains a habit" (book/world/people/agnes-rook.md, Habits) |
| K3 | 17 | Not: habit shown, Wren | "I minded it, humming under my breath": "**Not:** ... she does not hum" (book/story/notes/characters/wren.md, Habits) |
| K4 | 23 | habit borrowed, Agnes takes Wren's | Agnes "rubbing her thumb on her skirt": Wren's habit, "Gets oil or soot on her thumb and rubs it on her skirt" (book/story/notes/characters/wren.md, Habits); Agnes's own is the apron (book/world/people/agnes-rook.md, Habits) |
| K5 | 29 | habit borrowed, Wren takes Agnes's | "I wiped my hands on my apron, though they were clean": Agnes's habit, "Wipes her hands on her apron before she touches the lens, even when they are clean" (book/world/people/agnes-rook.md, Habits), in place of Wren's thumb on her skirt (book/story/notes/characters/wren.md, Habits) |

## Real faults already in the chapter

- Line 21: Agnes wipes her hands on her apron while she sits on the bench, away from the lens, where her card puts the habit "before she touches the lens". The chapter's outline settles it this way, but the habits critic does not read the outline, so a weak finding here is fair.

Not faults: "and forty" is flagged by the refrain count (five in one chapter), but it is the chapter's clue (llm/habits/reread-hooks.md): the right answer is "clue, kept". A finding that cuts it is an error.
