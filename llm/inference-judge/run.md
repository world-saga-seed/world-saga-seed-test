# Run: inference-judge

**Model:** Sonnet (the kit marks the judge Sonnet).

**How to run:** start a fresh session in this repo's top folder with that model, paste the block below (every `KIT/` replaced by the kit's folder, `../world-saga-seed/` or `../story-kit/`), and let it write its output, `runs/inference-judge/judge.md`. It must never see `llm/inference-judge/answers.md`. Then score it: `python3 llm/inference-judge/score.py runs/inference-judge/judge.md`.

**Filled for this book:** `{REPO}` is `book/`, with every path given from the repo's top folder. `{FINDS}` is [finds.md](finds.md), a finder list written for this test in the finder's form, some entries paired with evidence that does not carry them, as the kit warns. `{PROSE}` is this section's faulted copy of 00400. `{NOTES}` names the files the plot check reads (the book has no `plan/reread-hooks.md`, so the clue register is the notes' Clues line) and keeps the judge out of book/story/prose/ and book/reports/, which hold the unfaulted draft. The last line is added so the scorer can find the Breaks section and match by line.

```text
You judge a novel's first-person inferences, in the repo book/ (every path below is given from the repo's top folder). Read-only except your one output file. Run no git commands. Spawn no agents except at most 2 cheap assistants at a time for lookups (each writing nothing, spawning none).

The narrator is Wren Ashby, thirteen, the keeper's apprentice, telling in the first person what she lived. No chapter has another narrator. He may state only what he saw, heard, touched or was told, or his own thoughts; anything else needs its grounds.

Read the finder's list llm/inference-judge/finds.md. Its lines point at llm/inference-judge/chapter.md (chapter 00400, The forty minutes). For each entry, judge from the prose itself (open it at the line, read the paragraph and the two before), never the finder's gloss, which can be wrong or backwards. **The grounds must come first.** The telling is contemporaneous, so what grounds a claim must come before it or in its own sentence: a motive, feeling or past stated first and borne out later in the scene is still a break, since he could not know it when he said it.

**Check the plot before any break or question.** A line that looks unplanted, a slip or a contradiction is checked first against the chapter's notes and outline, the person's character sheet, the cards the notes link, the clue register, and a search of the ledger for the person or thing. A beat settled there passes, with its citation: an age on paper against an age by body may be the plot, and one object may go by two names. Only what the plot does not settle is a break or a question.

Sort each into one of:

1. **Grounded:** what he saw, heard or was told in the same beat supports it (a sign shown: a look, a callus, a word said). Pass silently.
2. **Known from before:** he could know it from an earlier chapter: something he was told, saw, or learned there. Before calling any break, search the earlier prose and the person's sheet for when he learned it. If found, pass it, citing file:line in one line.
3. **Common knowledge:** what any local knows (a trade's tools, a custom, what the town says). Pass silently.
4. **A verdict with no evidence** (a break): a person's past, trade or rank, a motive, what a thing is for, or a cause, stated with no grounds on the page and none from before.
5. **Someone else's inside as fact** (a break): another's feeling, thought or intent stated with no sign shown and none from before.
6. **Left to the reader on purpose** (a question for the writer): the page shows the signs and the narrator does not draw the conclusion, or draws one the reader may doubt; detail can be a red herring that follows the narrator's eye.

Write to runs/inference-judge/judge.md, headed "# Judge, inference", with:
- **Breaks** (4 and 5): file:line, the quote, which kind, why in one sentence (what you searched for grounds, and where), and a fix that gives the missing lead before the claim (a sign he saw, a word someone says, or his own read marked as his), in a few words. A cut only when the claim is incidental and nothing he could have seen would carry it.
- **Known from before** (2): one line each with the citation.
- **Questions** (6): file:line, the quote, both readings.
Then a tally. Do not rewrite any file. Inventing a finding is worse than missing one.

Run notes. The chapter's notes and outline are book/story/notes/00400-the-forty-minutes.md and book/story/outline/00400-the-forty-minutes.md; Wren's sheet is book/story/notes/characters/wren.md and her knowledge guard book/story/voice/knowledge/wren.md; the clue register is the Clues line of the chapter's notes (the book has no plan/reread-hooks.md); the ledger is book/plan/settled/ledger/. The only earlier prose is the 00200 scene, book/story/voice/samples/sample-pages.md. Do not open book/story/prose/ or book/reports/: they hold another draft of this chapter. Wren is the only narrator, and the writer did not write this chapter whole, so a break gets a fix.

Give every finding as a list item that begins `- line N:` with the line number in the input file. Here N is the line in llm/inference-judge/chapter.md. Give the breaks under a heading or bold label "Breaks", known from before under "Known from before", and questions under "Questions".
```
