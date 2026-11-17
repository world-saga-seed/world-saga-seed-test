# Facts critic

The facts critic (kit: plan/workflows/drafting/prompts/facts.md, Sonnet) asks where a chapter contradicts its notes, the settled lines of its outlines, the sheets, the cards, the rulings and the held facts, checking the narrator's lines against her knowledge guard first. The five plants in [chapter.md](chapter.md) test that it reads the settled lines and cards closely: a month, a keeper's years, the forty told outright, a reading that says twenty, and the causeway's hours; the guard's wrong beliefs must pass. It reads the chapter, book/story/notes/00400-the-forty-minutes.md, book/story/outline/00400-the-forty-minutes.md and 1-spring-tides.md, book/story/notes/characters/, book/world/, book/plan/settled/ledger/2027-03-02.md (the book's rulings), book/story/voice/pov.md, book/plan/reader-tests/answers.md, and [knowledge-00400.md](knowledge-00400.md) (tools/knowledge.py on the book's guard). The kit's Scale paragraph is left out: the book has no heights table, and the scale-finder section tests sizes. Paste [run.md](run.md) into a fresh Sonnet session in the repo's top folder; never show it [answers.md](answers.md).

Score a run: `python3 llm/score.py llm/facts/answers.md runs/facts/report.md`.

Baseline: not yet run.
