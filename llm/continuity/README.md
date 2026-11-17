# Continuity critic

The continuity critic (kit: plan/workflows/drafting/prompts/continuity.md, Sonnet) judges a batch page against page: names that change, people in two places, days and times that do not add up, phrases reused from an earlier chapter, a beat told twice, asks left hanging. The book has one drafted chapter, so the four plants in [chapter.md](chapter.md) test its seams against itself and against the one page before it, the oil-cart scene of 00200 (book/story/voice/samples/sample-pages.md): a tide time that runs backward, Saltby renamed, a sentence lifted from the oil cart, and a clue line said twice. It reads only the chapter and that sample, never the outlines or notes; the book keeps no volume digest, so the open-asks check has nothing to test here. Paste [run.md](run.md) into a fresh Sonnet session in the repo's top folder; never show it [answers.md](answers.md).

Score a run: `python3 llm/score.py llm/continuity/answers.md runs/continuity/report.md`.

Baseline: not yet run.
