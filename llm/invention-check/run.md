# Run: invention-check

**Model:** Sonnet (the kit names none; Sonnet is the default).

**How to run:** start a fresh session in this repo's top folder with that model, paste the block below (every `KIT/` replaced by the kit's folder, `../world-saga-seed/` or `../story-kit/`), and let it write its output, `runs/invention-check/report.md`. It must never see `llm/invention-check/answers.md`. Then score it: `python3 llm/score.py llm/invention-check/answers.md runs/invention-check/report.md`.

**Filled for this book:** `{REPO}` is `book/`, with every path given from the repo's top folder. `{LOG}` is [inventions.md](inventions.md), nine rows citing lines in [chapter.md](chapter.md). `{RULES}` is the book's README (the premise) and its ledger (the book has no separate rules file). The last line is added so the shared scorer can match each non-standing verdict by the chapter line its row cites.

```text
You are checking a list of small inventions for a novel in progress, in the folder book/ (every path below is given from the repo's top folder).
Every file is read-only except your one output file. Run no git commands. Do not launch
agents.

Read: llm/invention-check/inventions.md (the inventions, one row each: the new fact, file:line, the cards it touches,
who made it); for each row, the cited line in its file; the cards the row names; and the
setting's core rules, book/README.md (the premise) and book/plan/settled/ledger/2027-03-02.md (the settled rulings). Read nothing else.

For each row:
1. Against the canon: does the fact clash with any card it touches? Quote the card line.
2. Against what is to hand: could a person in that place, time and trade reach it with the
   tools, materials and knowledge they have? Would they think of it? For a custom or an
   institution: what pressure made it, and what came of the same pressure in real history?
3. Verdict: stands; reword (consistent in substance, a word or a part wrong; give the
   fix); break (a canon clash; give the canon line); or to the writer (it touches a
   settled line or a key frame, or it has no pressure and no precedent).

The question is whether each invention is consistent, not whether it is the best choice.
People in a story pick what they would think of, not the optimum.

Write a table to runs/invention-check/report.md: row number, the fact in a few words, verdict, the card line or fix,
one line of why. Finish with the counts by verdict.

Give every finding as a list item that begins `- line N:` with the line number in the input file. For this log, N is the line in llm/invention-check/chapter.md that the row cites; give one such item, after the table, for every row whose verdict is not "stands".
```
