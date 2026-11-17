# Key: voice and mechanism critic

*Never give this file to the model under test.* The input is [chapter.md](chapter.md): 00400 of *The Tide Clock* (draft 2) with one model tell, two voice faults, one hindsight line and one mechanism leak planted. Nothing else is changed.

**Pass:** 3 of 5 caught, at most 2 unmatched.

| ID | Line | Kind | Plant |
|---|---|---|---|
| K1 | 3 | tell, stock beat | "It was not a chore. It was a kind of prayer." added: the "It was not X. It was Y." beat, and a feeling named where the scene shows the work (book/story/voice/voice.md, The register) |
| K2 | 9 | voice, outside comparison | "as an actor runs his lines before the curtain goes up" for "as other people say grace": comparisons are "from her own life (the village, her grandmother, school, the house)" (book/story/voice/voice.md, The register); Wren has never seen a theater (book/story/notes/characters/wren.md, Voice: "Never from anything she has not seen") |
| K3 | 17 | voice, lining up clues | "So the forty was hers and not the almanac's, and it had to be the difference between the harbor's water and ours." added: "Wren notices; she does not explain" (book/story/voice/voice.md, The rule, R0302-02); it lets the reader state the tide outright, which is "Never said outright" (book/world/things/the-tide-table.md, On the page) |
| K4 | 23 | voice, hindsight | "It was a long while before I learned how wrong I was about Mrs. Rook." added: "Told as it happens: no 'later I learned'" (book/story/voice/voice.md, The rule, R0302-03; book/story/voice/pov.md, Time stance) |
| K5 | 29 | mechanism, held fact | "The sandbar off the holm held the water back, so the tide there ran behind the harbor's" added: the cause is author-side and "the page never explains it" (book/world/places/the-causeway.md, Why the water runs late), K3 is hidden (book/plan/reader-tests/key.md), and "sandbar" is banned (book/story/voice/banned.txt) |

## Real faults already in the chapter

- The chapter's measures sit below the sample's: and/s 0.49 against 0.94, sd 9.7 against 12.2 (llm/voice-mechanism/tells.txt; the unfaulted draft gives 0.49 and 9.9). Question 6 may fairly flag it as a candidate, severity taste; it names no single line, so wherever the report puts it, read it before calling it an invention.

Not faults: "And forty" each time, the weed a hand above the mud, and "By the almanac, low water had been an hour ago" are clues (llm/voice-mechanism/reread-hooks.md); a finding that cuts or varies one is an error.
