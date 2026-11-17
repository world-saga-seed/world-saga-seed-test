# Run: inference-finder

**Model:** Haiku (the kit marks the finder Haiku).

**How to run:** start a fresh session in this repo's top folder with that model, paste the block below (every `KIT/` replaced by the kit's folder, `../world-saga-seed/` or `../story-kit/`), and let it write its output, `runs/inference-finder/finds.md`. It must never see `llm/inference-finder/answers.md`. Then score it: `python3 llm/inference-finder/score.py runs/inference-finder/finds.md`.

**Filled for this book:** `{FILES}` is this section's faulted copy of 00400 (one chapter, where the kit runs two). `{NARRATOR}` names Wren, the book's one head. The line asking for `- line N:` items is added so the shared scorer can match findings by line.

```text
You are a finder for a novel's first-person check: how does the narrator know what he states? Read exactly these files: llm/inference-finder/chapter.md (chapter 00400). Read nothing else. Run no git commands. Spawn no agents.

The narrator is Wren Ashby, thirteen, the keeper's apprentice, telling in the first person what she lived. No chapter has another narrator.

List every line where the narrator states something he could only know by inference, or from inside someone else: a person's past, trade, age, health or rank; what someone feels, thinks, means, wants or knows; why someone did a thing; what a thing is for, where it came from, or how it works; a cause. Plain sight, sound and touch, and the narrator's own thoughts and feelings, are not inferences; skip them. Dialogue is skipped too: a speaker may claim anything.

For each, one entry: file:line; the quote (at most 15 words); what it claims, in a few words; and the evidence: quote at most 15 words from the same paragraph or the two before it that he saw, heard or was told and that the claim rests on, or write "none on the page". Do not judge whether the claim is right or allowed; only find it and pair it with its evidence.

Group by file. Write the list to runs/inference-finder/finds.md and finish with a count per file, and how many had "none on the page".

Give every finding as a list item that begins `- line N:` with the line number in the input file.
```
