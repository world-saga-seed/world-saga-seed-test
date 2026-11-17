# Run: fold-back

**Model:** Sonnet (the kit names none; Sonnet is the default).

**How to run:** start a fresh session in this repo's top folder with that model, paste the block below (every `KIT/` replaced by the kit's folder, `../world-saga-seed/` or `../story-kit/`), and let it write its output, `runs/fold-back/report.md, and the edits in runs/fold-back/book/`. It must never see `llm/fold-back/answers.md`. Then score it: `python3 llm/fold-back/score.py`.

**Filled for this book:** `{REPO}` is a scratch copy of book/ under runs/fold-back/, made by the setup, with this section's [prose.md](prose.md) and [notes.md](notes.md) in place of 00400's: the fold-back edits an outline and notes, and book/ stays untouched. runs/fold-back/ is this run's own output. `{CHAPTERS}` and `{GROUP}` are 00400; `{PAPER}` is [paper.md](paper.md); `{CHANGES}` is none. The book has no `plan/README.md`, no fold-back workflow and no `rulings.md`: the kit's plan-README template and fold-back workflow, and the book's ledger, stand in.

**Setup,** before the session starts:

```bash
rm -rf runs/fold-back && mkdir -p runs/fold-back && cp -r book runs/fold-back/book \
  && cp llm/fold-back/prose.md runs/fold-back/book/story/prose/00400-the-forty-minutes.md \
  && cp llm/fold-back/notes.md runs/fold-back/book/story/notes/00400-the-forty-minutes.md
```

```text
You are bringing a novel's outlines and notes up to date with its draft, in the folder
runs/fold-back/book/ (a scratch copy of book/ that the setup makes; every path below is given from the repo's top folder). Every file is read-only except the outlines and notes of your chapters. Run no git
commands; what changed since the draft is given to you below. Do not launch agents. Other sessions may have unsaved edits: never revert or reformat anything you did not
change, and edit by small exact replacements.

Your chapters: 00400. For each: the prose runs/fold-back/book/story/prose/N-*.md, the outline
runs/fold-back/book/story/outline/N-*.md and the notes runs/fold-back/book/story/notes/N-*.md. Write your report to runs/fold-back/report.md.

Read first: runs/fold-back/book/README.md; KIT/plan/templates/plan-README.md (the marks and the rules; the book has no plan/README.md);
KIT/plan/workflows/drafting/fold-back.md (the job, and the Next pass form);
runs/fold-back/book/plan/settled/ledger/2027-03-02.md (the book has no rulings.md); runs/fold-back/book/story/voice/voice.md. Then, for your chapters: the prose,
outline and notes in full; the batch paper llm/fold-back/paper.md; the drift rows in runs/fold-back/book/plan/state.md that
name your chapters; what changed in the notes and cards since the draft,
none: no commits to runs/fold-back/book/world/ or runs/fold-back/book/story/notes since the draft; and the cards and sheets for
everyone and everything on your pages.

Per chapter:
1. The draft into the outline and notes. Fold each choice the batch kept into the beat it
   belongs to, in one line, marked "(Proposal, from the draft, N.)" with N linked to the
   prose file. Do not copy prose into the outline; keep lore in the notes. Delete outline
   text the draft and its batch settled otherwise; deleting a "(Settled ...)" line needs a
   source that settles it, so if you have none, leave it and list the draft as drift. In
   the notes' "Open and flags", replace each item the draft answered with its answer,
   marked "(Answered by the draft, N; overturnable.)". Never fold a choice that
   contradicts a settled line: that is drift.
2. The Next pass list. Add "## Next pass" as the last section of the notes, in the form
   and kinds the workflow gives: drift, held, beat, voice (at most eight, the strongest),
   length. Every quote in backticks, copied exactly, 25 words at most, and it must
   resolve: copy the Next pass section to a scratch file, run python3 KIT/tools/quotes.py
   <that file> --in runs/fold-back/book/story/prose/N-*.md --backticks, and fix every miss.

Every line you add carries a mark. Delete stale text; do not strike it. Verify every link
and anchor you write. Never edit prose, cards, sheets, the arc outlines or runs/fold-back/book/plan/state.md;
put what they need in your report.

Report, headed "# Fold-back, 00400": by chapter, what you folded and the Next pass count
by kind; what shared files need (quote, file, why); state.md drift rows to delete or carry;
questions only the writer can answer, each with the plain option first and a
recommendation. Finish with a one-line tally.
```
