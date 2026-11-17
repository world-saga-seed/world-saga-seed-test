# Baseline: voice and mechanism critic

- **Model:** Sonnet (claude-sonnet-5-5), a cold run that ran `python3 llm/brief.py voice-mechanism` itself, 2026-11-17.
- **Score:** 5 of 5 caught, 1 unmatched: PASS (needs 3, at most 2 unmatched).
- **Unmatched, read:** the chapter's texture numbers below the sample's, the fair finding the key lists.
- **Clues:** the four planted clues of the book (C1 to C4) called "clue, kept", as they should be.
- **Snag:** the run's safety check refused book/plan/reader-tests/key.md, the book's reader key, which this prompt is meant to read, likely because it shares the name of the answer keys the run is told never to open. The run took the held facts from the POV file instead. To fix in the test repo: name the answer keys something no book file is named (`answers.md`).
- **Tokens:** about 49,000.
