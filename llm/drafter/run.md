# Run: drafter

**Model:** Sonnet (the kit names none; Sonnet is the default).

**How to run:** start a fresh session in this repo's top folder with that model, paste the block below (every `KIT/` replaced by the kit's folder, `../world-saga-seed/` or `../story-kit/`), and let it write its output, `runs/drafter/00700-caught-on-the-causeway.md, and the final report saved to runs/drafter/report.md`. It must never see `llm/drafter/answers.md`. Then score it: `python3 llm/drafter/score.py runs/drafter/00700-caught-on-the-causeway.md --report runs/drafter/report.md`.

**Filled for this book:** `{REPO}` is `book/`, with every path given from the repo's top folder. `{N}` is 00700, whose outline has two settled beats and the writer's missing frame; the book has no notes file for 00700, so its brief in the key-frames notes stands in. `{KNOWLEDGE}` is `tools/knowledge.py 00700 --dir book/story/voice/knowledge`, saved in this folder. The book has no `rulings.md`; its ledger stands in. `{PREV}` is none (00600 is not drafted); `{SKIM}` is 00400 and the 00200 sample. `{WORDS}` is a pilot's length, as 00400's is. `{EXTRA}` holds the missing frame and the brief's end state. The Scale paragraph is deleted, as the kit allows: the book has no heights table. The output is under runs/ rather than book/story/prose/.

```text
You are drafting one chapter of a novel in progress, in the folder book/ (every path below is given from the repo's top folder). Every file is
read-only except your one output file. Run no git commands of any kind (not even status or
stash): another session may be editing this folder. Do not launch agents.

Read, in this order:
1. the POV file, book/story/voice/pov-00700.md if it exists, else book/story/voice/pov.md (whose head,
   what each head may know, what is never told; where it and the voice sheet differ, it
   wins); then book/story/voice/voice.md (the voice sheet) and book/story/voice/banned.txt (the words
   the narration never uses), and the voice sheet of each head the POV file names, and llm/drafter/knowledge-00700.md, the
   entries in force at this chapter from each head's knowledge guard: what the head knows,
   believes wrongly and does not know. Where an entry turns in this chapter, put the beat
   where it changes on the page. Voice the wrong beliefs as the head's own, stated
   as plainly as the head would; never let the narration correct them or wink at them;
2. book/plan/settled/ledger/2027-03-02.md (the book's rulings: it has no rulings.md; every line binds you);
3. the style samples in book/story/voice/samples/: the voice as the writer set
   it. Match it; do not copy it;
4. the chapter's outline, book/story/outline/00700-caught-on-the-causeway.md (the numbered beats: what the page shows),
   and its notes for drafting, book/story/notes/1-spring-tides-key-frames.md, the section "Brief: 00700, Caught on the causeway" (the book has no notes file for 00700);
5. the arc outline book/story/outline/1-spring-tides.md, for context only;
6. the draft before it, none (00600 is not drafted; its line in the arc outline is the join), read closely for the join; and skim book/story/prose/00400-the-forty-minutes.md and book/story/voice/samples/sample-pages.md for the people,
   places and objects already set;
7. the cards for every person, place and thing in the chapter, through the indexes in
   book/world/*/README.md, and the sheets in book/story/notes/characters/. Read the Habits section of
   everyone who appears, and give each person only their own.
Read nothing else. Do not read any outline after this chapter.

Follow a link in the outline only as far as you need to get a fact right. The notes are the
facts; the page shows only what the narrator sees and what the scene needs. Lore stays in
the notes.

Write the chapter as prose into runs/drafter/00700-caught-on-the-causeway.md, replacing any earlier draft,
with the title line "# Caught on the Causeway (draft 1)". Every settled beat, in order; the proposal
beats too, unless one contradicts a settled beat; nothing the outline marks author-side or
reference. The chapter falls after key frame 3, 00500 (Wren sees that Agnes cannot see the lines in the log); this chapter is key frame 4. Length: 1,200 to 1,800 words (a pilot, as 00400's is; the full chapter's 5,000 to 6,000 come later), a target, not a cap.

Keep to the texture in the rulings: measure with
  python3 KIT/tools/tells.py runs/drafter/00700-caught-on-the-causeway.md --banned book/story/voice/banned.txt
and fix every banned-word hit that is narration.

No notes, marks or comments inside the prose file. Where a beat cannot be written without
inventing a fact the notes lack, write around it and list it.

The outline's third beat is the writer's missing frame: what Agnes says when Wren asks her about "and forty". Do not write her answer: write around it, and list it under the facts you left open. The brief's end state holds: the inspector safe on the holm, wet to the waist; Wren knowing what "and forty" means; Agnes's secret still kept. Dell fetching the inspector back with the cart is only proposed.

Finish with a short report:
- the word count and the tells.py line;
- the beats covered; any beat skipped or changed, and why;
- Inventions: the small things you made up (names, objects, staging, sayings), one line
  each: the fact, its line, the cards it touches. Do not check them yourself; a separate
  run does;
- the facts you had to leave open;
- the banned-word hits you fixed.
```
