# Run: out-of-world phrase finder

**Model:** Sonnet. The kit's prompt (`plan/workflows/drafting/prompts/idioms.md`, v1) is not marked Haiku.

**How to run:** start a fresh session in this repo's top folder with that model, paste the block below, and let it write its report. It must never see `llm/idioms/answers.md` or `llm/idioms/chapter.md`. Then score it: `python3 llm/score.py llm/idioms/answers.md runs/idioms/report.md`.

**Filled for this book:** the kit says to strip the dialogue first, so `{THREAD}` is [narration.md](narration.md): this section's faulted [chapter.md](chapter.md) with every quoted span replaced by `[…]`, line for line, so its line numbers are the chapter's. `{NARRATOR}` and the one line on who she is come from Wren's sheet and the book's premise, saying what she knows and not what to look for. `{EXTRA_KINDS}` is empty and its line is deleted. `{RANGE}` is 00400.

```text
You are reading a novel narrated by Wren Ashby: a girl of thirteen around 1890, raised by
her grandmother in Saltby, a village with a harbor on a northern coast, and apprenticed since the
autumn to the keeper of the light on the tidal island off it; she has been to the village
school and has never been farther than the village and the island, nor seen or heard of
anything the century after hers would bring. Read only llm/idioms/narration.md (the chapter's narration, line for line with the
chapter, so its line numbers are the chapter's); do not read anything else.

List every phrase in the narration that only makes sense to someone outside that world:
- idioms and stock phrases that carry a picture from elsewhere;
- animals, machines, sports, foods, money, stories, places, measures and units of time
  the narrator could not know;
- single words that carry an outside picture (for example, a modern word in a
  historical narrator's mouth);

Dialogue counts only when Wren Ashby speaks it. Do not list plain words with an innocent
sense unless the sense here is the outside one.

For each: the exact quote, 25 words at most; its line; the outside picture it carries; and
one shifted phrasing the narrator could say instead, built from their own world, not a
synonym. If you find nothing, say so; inventing a finding is worse than missing one.

Write your list to runs/idioms/report.md, headed "# Out-of-world phrases in 00400", numbered. Run no git
commands. Do not launch agents. Every file is read-only except that output file.
Write your report to runs/idioms/report.md. Give every finding as a list item that begins `- line N:` with the line number in the chapter file.
```
