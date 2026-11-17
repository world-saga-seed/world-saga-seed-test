# Baseline: inference finder

- **Model:** Haiku (claude-haiku-5-5), a cold run that ran `python3 llm/brief.py inference-finder` itself, 2026-11-17.
- **Score:** 5 of 5 plants listed (17 finds, 11 "none on the page"), but both grounded near misses listed with "none on the page" (3 entries): FAIL on the near-miss rule.
- **Reading:** the finder's known weakness, and the reason for the kit's rule that the judge reads every find: it pairs a claim with the wrong evidence or none, missing grounds a line earlier. It is a finder; the pair is scored by the judge's section.
- **Tokens:** about 48,000.
