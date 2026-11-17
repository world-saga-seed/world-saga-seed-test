# Run: outline-critic

**Model:** Sonnet (the kit names none; Sonnet is the default).

**How to run:** start a fresh session in this repo's top folder with that model, paste the block below (every `KIT/` replaced by the kit's folder, `../world-saga-seed/` or `../story-kit/`), and let it write its output, `runs/outline-critic/report.md`. It must never see `llm/outline-critic/answers.md`. Then score it: `python3 llm/score.py llm/outline-critic/answers.md runs/outline-critic/report.md`.

**Filled for this book:** `{REPO}` is `book/`, with every path given from the repo's top folder. `{N}` and `{RANGE}` are 00400, and the outline is this section's faulted copy, so the prompt's `story/outline/{N}-*.md` names it and tells the critic not to open the book's own. The book has no `rulings.md`; its ledger stands in. `{ARC}` is book/story/outline/1-spring-tides.md.

```text
You are a critic for a novel in progress, in the folder book/ (every path below is given from the repo's top folder). Where does this outline
contradict the notes, or give a beat no cause? Every file is read-only except your one
output file. Run no git commands. Do not launch agents.

The outlines: llm/outline-critic/outline.md (it stands for book/story/outline/00400-*.md; do not open that file, which is another copy) for the chapters 00400. Judge them against:
- their notes, book/story/notes/00400-the-forty-minutes.md, and the arc outline book/story/outline/1-spring-tides.md;
- the sheets in book/story/notes/characters/ for everyone in them;
- the cards in book/world/ (each folder has a README index), followed from links only as far as
  a fact needs;
- book/plan/settled/ledger/2027-03-02.md, whose lines are settled (the book has no rulings.md).
Do not read drafted prose of these chapters or any later outline.

Two questions:
1. Contradiction. Where does a beat contradict a settled line in the notes, cards or
   rulings?
2. Cause. Where does a beat happen with no cause in the notes or an earlier beat: help that
   arrives on cue, a person acting from convenience, a power used once that would solve
   later problems too?

Report each finding as:
- quote: the exact text, 25 words at most
- file and line
- kind: contradiction or cause
- against: the note's own words, quoted, with its file and heading (for a cause: what rule
  or earlier beat it would need)
- why: one sentence
- severity: break, weak, or taste
- direction: one line

Do not rewrite the outline. Do not praise. If you find nothing, say "No findings"; inventing
a finding is worse than missing one. Write the findings to runs/outline-critic/report.md, headed
"# Critic: outline, 00400", numbered, and finish with a one-line tally.

Give every finding as a list item that begins `- line N:` with the line number in the input file.
```
