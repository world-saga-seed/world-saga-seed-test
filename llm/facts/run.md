# Run: facts critic

**Model:** Sonnet. The kit's prompt (`plan/workflows/drafting/prompts/facts.md`, v3) is a critic, not a Haiku finder.

**How to run:** start a fresh session in this repo's top folder with that model, paste the block below, and let it write its report. It must never see `llm/facts/answers.md`. Then score it: `python3 llm/score.py llm/facts/answers.md runs/facts/report.md`.

**Filled for this book:** `{REPO}` is `book/`, with every path given from the repo's top folder; the chapter is this section's faulted copy. `{READ_BEFORE}` is none (00400 is the only drafted chapter). The book has no `rulings.md`; its settled rulings are its ledger, so that file stands in. `{BATCH_NOTES}` is empty and its line is deleted. The Scale paragraph is deleted: the book has no heights table (the scale-finder section tests sizes with an invented one). `{KNOWLEDGE}` is `tools/knowledge.py 00400 --dir book/story/voice/knowledge`, saved in this folder.

```text
You are a critic for a novel in progress, in the folder book/ (every path below is given
from the repo's top folder). Where does this chapter contradict the notes? Every file is
read-only except your one output file. Run no git commands. Do not launch agents.

The chapter: llm/facts/chapter.md (chapter 00400). Judge it against:
- its notes for drafting, book/story/notes/00400-the-forty-minutes.md;
- the settled lines (marked "(Settled ...)", not the proposals) in its outline,
  book/story/outline/00400-the-forty-minutes.md, and in the arc outline
  book/story/outline/1-spring-tides.md;
- the sheets in book/story/notes/characters/ for everyone who appears;
- the cards in book/world/ (each folder has a README index), followed from links only as
  far as a fact needs;
- book/plan/settled/ledger/2027-03-02.md, whose lines are settled;
- the drafts before it (none: 00400 is the first chapter of this book drafted): what they
  put on the page is settled too.
Read the POV file first: book/story/voice/pov-00400.md if it exists, else
book/story/voice/pov.md; it names the heads the narration is in.
Do not read any later outline. Judge only facts: ignore voice, style, pacing and taste.

Knowledge guards. llm/facts/knowledge-00400.md holds what each narrating head knows,
believes wrongly and does not know at this chapter, the entries in force from its guard in
book/story/voice/knowledge/. An entry marked as turning in this chapter holds up to the beat
where it changes. Check every line of a head's narration against it before the cards and
sheets:
- a line that matches an entry under Believes is the narrator's own wrong belief, kept on
  purpose: it is not a finding, and never direct that it be corrected;
- a line wrong against the cards, sheets or notes and listed nowhere in the guard is weak:
  why "unlisted error: a drafter's slip, or a new belief", direction "writer to rule: fix
  it, or list it as a belief";
- a line that states something under Does not know is a break, and so is a line that
  contradicts an entry under Knows.
A book with no guard for a head judges that head by the cards alone.

Held facts. The reader key, book/plan/reader-tests/key.md, lists what the reader must not
get (its hidden and forbidden entries), and the outline marks author-side lines. A line
that states a held fact, or lets a reader state one, is a break, whoever narrates.

Report each finding as:
- quote: the exact text, copied character for character, 25 words at most
- file and line
- against: the note's own words, quoted, with its file and heading
- why: one sentence
- severity: break (contradicts a settled fact), weak (strains one, or rests on a proposal
  against a settled line), or taste
- direction: one line

Do not rewrite the text. Do not praise. If you find nothing, say "No findings"; that is an
acceptable answer, and inventing a finding is worse than missing one. Write the findings to
runs/facts/report.md, headed "# Critic: facts, 00400", numbered, and finish with a one-line tally.
Write your report to runs/facts/report.md. Give every finding as a list item that begins `- line N:` with the line number in the chapter file.
```
