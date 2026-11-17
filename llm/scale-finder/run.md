# Run: scale finder

**Model:** Haiku. The kit's prompt (`plan/workflows/drafting/prompts/scale-finder.md`) is marked Haiku: a finder that lists, for the facts critic to judge.

**How to run:** start a fresh session in this repo's top folder with that model, paste the block below, and let it write its list. It must never see `llm/scale-finder/answers.md`. Then score it: `python3 llm/score.py llm/scale-finder/answers.md runs/scale-finder/report.md`.

**Filled for this book:** `{FILES}` is this section's faulted copy of 00400. The book has no heights table, so the heights (Wren 150 cm, Agnes 152 cm) and [size-facts.txt](size-facts.txt) are invented for this section, and `{HEIGHTS}` is the head of `tools/scale.py 00400 --height 150 --other Agnes=152 --facts llm/scale-finder/size-facts.txt` (its list of size phrases left off, since that is what the finder must find). `{OUT}` is the report file.

```text
You are a finder for a novel's scale check. Read exactly these files: llm/scale-finder/chapter.md. Read nothing else. Run no git commands. Spawn no agents.

# Scale sheet, 00400

- **Viewpoint:** about 150 cm.
- **Agnes:** 152 cm, 0.2 hands taller.
- **On the viewpoint's body:** eyes 140, chin 130, shoulder 123, chest 108, waist 90, hip 75, knee 42 cm.
- **A hand** is about 9 cm; the lamp-room floor to the lens's top ring is about 220 cm, so a girl of 150 cm needs the 30 cm step stool to reach it; the gallery rail is 110 cm high; the gallery bench seat is 40 cm off the floor; the third post stands about 150 cm above the mud.
- **The rule:** a size on the page is measured from the one who sees it, at the height above, and from the card of the object or creature; vary the reference from the chapters either side.

List every line that states or implies a size, a height, a reach or a fit: explicit sizes ("at the height of my chest", "taller than a man") and implied ones, shown by action ("reached up for the latch", "could see over the wall", "ducked under", "his hand swallowed mine", "climbed onto the stool to reach", "feet did not reach the floor"). Do not judge whether they are right; only find them.

For each, one line: file:line, the quote (at most 15 words), and what it implies in a few words. Group by file. Write the list to runs/scale-finder/report.md and finish with a count per file.
Write your report to runs/scale-finder/report.md. Give every finding as a list item that begins `- line N:` with the line number in the chapter file.
```
