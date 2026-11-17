# Baseline: reviser

- **Model:** Sonnet (claude-sonnet-5-5), a cold run that ran `python3 llm/brief.py reviser` itself after the setup, 2026-11-17.
- **Score:** 4 of 4 faults gone, 4 of 4 keep lines intact, title unchanged, 0 checks failed: PASS.
- **Scope:** the diff against the faulted draft is three lines, each a finding's own; nothing else moved. Texture after: and/s 0.49, sd 10.0, 0 banned hits.
- **Tokens:** about 44,000.
