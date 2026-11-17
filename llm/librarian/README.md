# Librarian

The librarian (kit: plan/workflows/drafting/prompts/librarian.md, the smallest model, so Haiku) answers lookups from the notes with a quoted path:line, and says "Not in the notes" rather than guess. [questions.md](questions.md) holds eight: six answered in book/'s cards and sheet (one whose answer is a proposal, to test that it says so) and two the notes never answer (the inspector's name; who first found the forty, which tempts "Agnes"). Paste [run.md](run.md) into a fresh Haiku session in the repo's top folder and save its final message to runs/librarian/answers.md; never show it [answers.md](answers.md). [score.py](score.py) checks each answer for the key's patterns and its path; a hand-made set of eight right answers passes, and the same set with "Agnes" for question 8 fails.

Score a run: `python3 llm/librarian/score.py runs/librarian/answers.md`

Baseline: not yet run.
