# Reviser

The reviser (kit: plan/workflows/drafting/prompts/reviser.md; the kit names no model, so Sonnet) fixes verified findings by changing wording only, keeping every clue and keep-list line. [chapter.md](chapter.md) is 00400 with four faults written back in (hindsight, a banned phrase, the causeway's hours, the clue's echo); [findings.md](findings.md) names them; [keep.md](keep.md) holds four lines that must survive word for word, one on the same line as the echo to be cut. The setup in [run.md](run.md) copies the chapter to runs/reviser/, which the reviser edits; paste the block into a fresh Sonnet session in the repo's top folder; never show it [answers.md](answers.md). [score.py](score.py) checks each fault gone, each keep line present (kit tools/quotes.py) and the title unchanged; it fails all four faults on the faulted chapter and passes the book's own draft 2.

Score a run: `python3 llm/reviser/score.py runs/reviser/00400-the-forty-minutes.md`

Baseline: not yet run.
