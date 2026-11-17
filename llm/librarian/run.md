# Run: librarian

**Model:** Haiku (the kit: "the smallest model").

**How to run:** start a fresh session in this repo's top folder with that model, paste the block below (every `KIT/` replaced by the kit's folder, `../world-saga-seed/` or `../story-kit/`), and let it write its output, `runs/librarian/answers.md (the librarian writes no file: save its final message there)`. It must never see `llm/librarian/answers.md`. Then score it: `python3 llm/librarian/score.py runs/librarian/answers.md`.

**Filled for this book:** `{REPO}` is `book/`, with every path given from the repo's top folder. `{QUESTIONS}` are [questions.md](questions.md). The book has no tools/, so the cards.py line runs the kit's copy on book/world. The last line numbers the answers for score.py.

```text
You are a librarian for a novel's notes, in the folder book/ (every path below is given from the repo's top folder). Read-only: write no file, run
no git, launch no agents. Answer each question below from the notes, quoting the line that
answers it with its path:line, so the asker can check it.

How to look: first book/world/INDEX.md (the subject index, A to Z: grep it for the subject),
then python3 KIT/tools/cards.py find WORDS --root book/world (cards whose head, then text, holds the words), then
grep the card folders and book/story/notes/characters/. Read only the card or section that
answers; do not read prose chapters or plan files. Prefer a line marked (Settled ...) over
a proposal or a reading, and say which it is. If the notes do not answer, say "Not in the
notes" and name the closest card; never guess or infer past what the line says. Keep each
answer under 80 words.

Questions:
1. How many years has Agnes Rook kept the Skerry Holm light?
2. How long is the causeway bare at each low water?
3. How many marker posts does the causeway have, and which one shows how long the water has been off?
4. Who brings the new almanac each year, and in what month?
5. What does Wren do when she gets oil or soot on her thumb, and is that settled or a proposal?
6. Where in the lighthouse is the log book kept?
7. What is the Board inspector's name?
8. Who first found that the holm's water runs forty minutes late?

Begin each answer with its number, `A1:` to `A8:`.
```
