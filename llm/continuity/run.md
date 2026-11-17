# Run: continuity critic

**Model:** Sonnet. The kit's prompt (`plan/workflows/drafting/prompts/continuity.md`, v2) is a critic, not a Haiku finder.

**How to run:** start a fresh session in this repo's top folder with that model, paste the block below, and let it write its report. It must never see `llm/continuity/answers.md`. Then score it: `python3 llm/score.py llm/continuity/answers.md runs/continuity/report.md`.

**Filled for this book:** `{REPO}` is `book/`, with every path given from the repo's top folder. The book has one drafted chapter, so `{CHAPTERS}` is this section's faulted copy of 00400 and `{READ_BEFORE}` is the only page before it: the writer's oil-cart scene, which chapter 00200 is built from (the book's style sample). The book keeps no volume digest, so `{DIGEST}` is given as none. `{RANGE}` is 00400.

```text
You are a critic for a novel in progress, in the folder book/ (every path below is given
from the repo's top folder). Where do these chapters disagree with the chapters before
them, and with each other? Every file is read-only except your one output file. Run no git
commands. Do not launch agents.

The chapters: llm/continuity/chapter.md (chapter 00400). They were drafted side by side (each drafter had only the outline
of the chapter before, not its draft), so the seams between them are the first thing to
check: who is where, what was given when, which days, what each person already knows, what
each has already seen. Then check them against the drafts before: read
book/story/voice/samples/sample-pages.md (the oil-cart scene of 00200, the page before).

Do not read the outlines or the notes: judge the page against the page. Flag:
- names and terms that change between chapters (the earlier page's names win);
- people who act as if they had not met, or had not seen what they have;
- days, times and distances that do not add up;
- objects in two places, or gone and back;
- phrases or whole sentences reused from an earlier chapter;
- a beat told twice;
- an ask left hanging: a request, promise or question someone put that a later page
  should answer and does not, or answers as if it were never asked. The volume digest's
  "Open asks" (none: this book keeps no volume digest yet) lists the asks still open from earlier chapters: flag one these
  chapters answer wrongly or forget at a moment that calls for it.

Report each finding as:
- quote: the exact text, 25 words at most
- file and line
- against: the earlier text, quoted, with its file and line
- why: one sentence
- severity: break, weak, or taste
- direction: one line

Do not rewrite the text. Do not praise. If you find nothing, say "No findings"; inventing a
finding is worse than missing one. Write the findings to runs/continuity/report.md, headed
"# Critic: continuity, 00400", numbered, and finish with a one-line tally.
Write your report to runs/continuity/report.md. Give every finding as a list item that begins `- line N:` with the line number in the chapter file.
```
