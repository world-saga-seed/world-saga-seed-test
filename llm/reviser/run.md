# Run: reviser

**Model:** Sonnet (the kit names none; Sonnet is the default).

**How to run:** start a fresh session in this repo's top folder with that model, paste the block below (every `KIT/` replaced by the kit's folder, `../world-saga-seed/` or `../story-kit/`), and let it write its output, `runs/reviser/00400-the-forty-minutes.md (revised in place), and the final report saved to runs/reviser/report.md`. It must never see `llm/reviser/answers.md`. Then score it: `python3 llm/reviser/score.py runs/reviser/00400-the-forty-minutes.md`.

**Filled for this book:** `{REPO}` is `book/`, with every path given from the repo's top folder. `{CHAPTERS}` is a copy of this section's faulted draft, made by the setup, so the reviser edits runs/ and never llm/. `{FINDINGS}`, `{KEEP}` and `{PAPER}` are this folder's findings.md, keep.md and paper.md. `{KNOWLEDGE}` is `tools/knowledge.py 00400 --dir book/story/voice/knowledge`, saved in this folder. The book has no `rulings.md` (its ledger stands in) and no `plan/reread-hooks.md` (the notes' Clues line is the register). `{WORDS}` is the pilot's range.

**Setup,** before the session starts:

```bash
mkdir -p runs/reviser && cp llm/reviser/chapter.md runs/reviser/00400-the-forty-minutes.md
```

```text
You are revising chapters of a novel in progress, in the folder book/ (every path below is given from the repo's top folder), on verified critic
findings. Every file is read-only except these: runs/reviser/00400-the-forty-minutes.md. Run no git commands of any kind.
Do not launch agents.

Read: book/story/voice/voice.md, book/story/voice/banned.txt and book/plan/settled/ledger/2027-03-02.md
(the rules; the book has no rulings.md); two or three of the style samples in book/story/voice/samples/;
the verified findings, llm/reviser/findings.md (its chapter.md lines are the lines of runs/reviser/00400-the-forty-minutes.md); the keep list, llm/reviser/keep.md; and the batch paper, llm/reviser/paper.md,
whose fixes section lists every fix already made on these chapters. Do not undo any of
those fixes; some quotes in the findings may have changed because of them.

Address every finding on the list: cut, trim or make plain, as the direction says, or by a
better cut of your own that meets the same point. Where a finding's quote is already gone,
say so and move on. Each beat said once; no sentence reused across the chapters or from
earlier chapters; the narrator never lines up the plot for the reader.

Rules:
- Change wording only. Add no fact, object, person, name or event; move no beat. Where a
  cut leaves a gap, close it with a few plain words.
- For a finding on how the narrator knows: give the lead before the claim, either the
  sign the scene already shows, moved first, or his read marked as his ("I thought").
  A new sign or spoken line only where the finding's fix was approved by the writer.
  Cut only when nothing he could have seen would carry it.
- Keep every line of dialogue unless a finding names it.
- Keep every line on the keep list exactly.
- Never cut or reword a clue: a line in a chapter's clue notes (book/story/notes/00400-the-forty-minutes.md, Clues; the book has no plan/reread-hooks.md), or
  any name, order or number a reader could solve the story from. Where a finding asks for
  that cut, keep the clue and say so.
- Never correct a narrator's listed belief: a line that matches an entry under Believes
  in llm/reviser/knowledge-00400.md is wrong on purpose. Where a finding asks for that
  fix, keep the line and say so.
- Keep each chapter inside the texture of the samples, measured with
  python3 KIT/tools/tells.py <file>. Do not chop. Split every sentence tells.py prints as a
  "knot" that runs two main clauses through a semicolon.
- Word ranges: 00400: 450 to 600. Do not cut below; if the findings force it, say so.
- Everything in the rulings holds.
- When done, run python3 KIT/tools/tells.py <file> --banned book/story/voice/banned.txt and fix any
  narration hit.

Finish with a short report: each finding by number and what you did (or why you left it);
for each chapter the word count and the tells.py line, before and after; then an
Inventions list of any fact you added that the notes lack (expected: none), one line each:
the fact, the line, the cards it touches.
```
