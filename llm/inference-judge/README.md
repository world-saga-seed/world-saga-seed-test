# Inference judge

The inference judge (kit: plan/workflows/drafting/prompts/inference-judge.md, Sonnet) sorts a finder's list into breaks, known from before, common knowledge and questions, from the prose itself and the plot. It judges [finds.md](finds.md), a finder list on [chapter.md](chapter.md) (the inference finder's faulted 00400) in which four of the five plants come paired with evidence that does not carry them, and two near misses with the true grounds a line earlier; a break on a near miss is an error, and so is a break on Wren's listed wrong belief. Paste [run.md](run.md) into a fresh Sonnet session in the repo's top folder; never show it [answers.md](answers.md). The section's [score.py](score.py) scores the report's Breaks section only, counts near-miss breaks as errors, and lists plants sent to Questions as softened.

Score a run: `python3 llm/inference-judge/score.py runs/inference-judge/judge.md`

Baseline: not yet run.
