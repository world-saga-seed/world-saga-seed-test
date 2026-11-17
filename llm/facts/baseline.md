# Baseline: facts critic

- **Model:** Sonnet (claude-sonnet-5-5), a cold run from `python3 llm/brief.py facts`, 2026-11-17.
- **Score:** 5 of 5 caught, 0 unmatched: PASS (needs 3, at most 2 unmatched).
- **Tokens:** about 51,000 for the run.
- **Not raised:** the real fault the key lists as fair (line 17, the almanac as the only other book), neither caught nor scored.
- **Note:** on its first command the run tried to open this section's key.md; the session's permissions refused it, and the report rests on the book's files. Run the prompts where the key cannot be read (a fresh clone without `llm/*/key.md`, or a permission rule), not on the instruction alone.
