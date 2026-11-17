# Coverage and slip critic

The coverage and slip critic (kit: plan/workflows/drafting/prompts/coverage-slip.md, Sonnet) asks which of the outline's beats are missing, out of order or added, and where the narration knows what its head cannot have. The five plants in [chapter.md](chapter.md) test both halves: three settled beats contradicted (the opening on the day, "No explanation", the hands wiped before she has touched anything) and two slips (Agnes's fear and failing eyes told as fact, and Wren knowing the forty minutes before the crossing). It reads the chapter, book/story/outline/00400-the-forty-minutes.md (beats only), book/story/voice/pov.md and voice.md, book/plan/settled/ledger/2027-03-02.md (the book's rulings), book/plan/reader-tests/answers.md, and [knowledge-00400.md](knowledge-00400.md); never the notes. Paste [run.md](run.md) into a fresh Sonnet session in the repo's top folder; never show it [answers.md](answers.md).

Score a run: `python3 llm/score.py llm/coverage-slip/answers.md runs/coverage-slip/report.md`.

Baseline: not yet run.
