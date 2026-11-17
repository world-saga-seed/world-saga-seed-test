# Baseline: attribution test

- **Model:** Sonnet (claude-sonnet-5-5), a cold run that ran `python3 llm/brief.py attribution` itself, 2026-11-17.
- **Score:** 14 of 14 clean paragraphs right, the plant missed, 1 false flag (P2, "could be either"): FAIL.
- **Reading:** a real miss. P4, Agnes's head written in Wren's voice, was given to Agnes as "sure": the reader went by what the paragraph is about, not how it is told, so the bleed passed. The prompt may need to ask for the voice first (which head talks like this?) and the content second.
- **Scorer fixed on this run:** "None seemed wrong" had been read as a flag, and a flag word marked every paragraph in its sentence; flags now count by clause, negations dropped.
- **Tokens:** about 41,000.
