# Run: procedures critic

**Model:** Sonnet. The kit's prompt (`plan/workflows/drafting/prompts/procedures.md`, v1) is a critic, not a Haiku finder.

**How to run:** start a fresh session in this repo's top folder with that model, paste the block below, and let it write its report. It must never see `llm/procedures/answers.md`. Then score it: `python3 llm/score.py llm/procedures/answers.md runs/procedures/report.md`.

**Filled for this book:** `{REPO}` is `book/`, with every path given from the repo's top folder; the chapter is this section's faulted copy. The book has no lens card (its reader key says so), so [the-lens.md](the-lens.md) here is an invented card that sets the cleaning step by step, written to agree with the unfaulted chapter. `{INDEX}` is this book's three carded processes. `{READ_BEFORE}` is none (00400 is the only drafted chapter). `{BATCH_NOTES}` is empty. The book keeps no volume digest, so `{DIGEST}` is given as none.

```text
You are a critic for a novel in progress, in the folder book/ (every path below is given
from the repo's top folder). Is every procedure on the page done as the setting's cards
set it? Every file is read-only except your one output file. Run no git commands. Do not
launch agents.

The chapter: llm/procedures/chapter.md (chapter 00400). A missing step is your main quarry: a tool used before
it is fetched, a door passed with no key shown, a step done out of the order the card
sets.

1. List every act on the page that a process in the cards covers: a trade at work, a
   journey's stages, papers, payments and counters, a rite, a fight's order, a camp or a
   watch, an animal handled, a day counted. Quote the line for each.
2. For each, find the process's card and walk it on paper, step by step, against the page:
   what must happen first, what tool or hand it takes, what must not be done. Where each
   process is carded:
   - cleaning the lens: llm/procedures/the-lens.md (When; Before the glass is touched;
     The tools; The order; Each ring; The bull's-eye)
   - reading the tides aloud: book/world/things/the-tide-table.md (The clue) and
     book/world/people/agnes-rook.md (Habits)
   - crossing the causeway, and the posts: book/world/places/the-causeway.md (What it is;
     The posts; The danger)
   - the watch and its log: book/world/things/the-log-book.md (What it is; Who writes it)
   The drafts before it (none: 00400 is the first chapter of this book drafted) are settled facts too: a step shown there is how it
   is done.
   The volume digest's "Routines shown in full" (none: this book keeps no volume digest yet) lists each routine with the
   chapters that already show it step by step: a routine shown in full a third time in the
   volume is a finding at weak, direction: a line or two of scaffolding, and this showing's
   own event kept whole.
3. Judge only procedure: ignore voice, style, pacing and taste. A step the page does not
   show, where showing it is not needed and nothing on the page contradicts it, is no
   finding; a step whose absence the page makes visible (a hand on the thing, a body
   walking through) is.

Report each finding as:
- quote: the exact text, copied character for character, 25 words at most
- file and line
- against: the card's own words, quoted, with its file and heading
- why: one sentence naming the step skipped, misordered or done by the wrong hand
- severity: break (contradicts a settled step), weak (strains one, or rests on a
  proposal), or taste
- direction: one line

Do not rewrite the text. Do not praise. If you find nothing, say "No findings"; inventing a
finding is worse than missing one. Write the findings to runs/procedures/report.md, headed
"# Critic: procedures, 00400", numbered, and finish with a one-line tally and the list of
acts you walked.
Write your report to runs/procedures/report.md. Give every finding as a list item that begins `- line N:` with the line number in the chapter file.
```
