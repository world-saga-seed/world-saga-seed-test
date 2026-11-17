# Run: habits critic

**Model:** Sonnet. The kit's prompt (`plan/workflows/drafting/prompts/habits.md`, v3) is a critic, not a Haiku finder.

**How to run:** start a fresh session in this repo's top folder with that model, paste the block below, and let it write its report. It must never see `llm/habits/answers.md`. Then score it: `python3 llm/score.py llm/habits/answers.md runs/habits/report.md`.

**Filled for this book:** `{REPO}` is `book/`, with every path given from the repo's top folder; `{CHAPTERS}` is this section's faulted copy of 00400. The book keeps no refrains watch list, so [refrains.txt](refrains.txt) here is the smallest one (the three habits its sheet and card record), and `{REFRAINS}` is `tools/refrains.py llm/habits/chapter.md --list llm/habits/refrains.txt`, saved as [refrains-00400.md](refrains-00400.md) and pasted in. The book has no `plan/reread-hooks.md`; [reread-hooks.md](reread-hooks.md) in this folder is the smallest clue register for 00400, copied from its notes' clue line. `{RANGE}` is 00400.

```text
You are a critic for a novel in progress, in the folder book/ (every path below is given
from the repo's top folder). Every file is read-only except your one output file. Run no
git commands. Do not launch agents.

The chapters: llm/habits/chapter.md (chapter 00400). Where does someone in these chapters do a habit that is not
theirs, break one of theirs, or show one their sheet says they do not have? Where does a
habit repeat so often it reads as filler?

Read the Habits section of the sheet in book/story/notes/characters/ for everyone who appears,
the Habits line of any card in book/world/people/ for others who appear, and book/story/voice/voice.md
for the narrator's own habits of attention and telling. A "Not:" line on a sheet records a
habit the person does not have. People with no sheet or card: flag only a habit borrowed
from someone who has one. Do not read the outlines or the notes for drafting.

Refrains across the volume. The count below is the count of the volume's refrains from its
first chapter to these (tools/refrains.py), with every six-word run found nearly word for
word in three chapters or more:

# Refrains, chapter to chapter

| Refrain | Volume | Per chapter | Flag |
|---|---|---|---|
| thumb on skirt | 1 | chapter 1 |  |
| apron | 2 | chapter 2 |  |
| and forty | 5 | chapter 5 | chapter: 5 |

## Near-verbatim in three chapters or more (a six-word run shared)

None.

A refrain flagged there that shows in these chapters is a
finding: name which showings to keep whole (the first, a farewell, a showing that changes
something) and which to cut to a gesture or a word, since a reader who has the picture
feels the shorthand as momentum. A description repeated near word for word at each showing
is weak. A habit the writer has kept on purpose past the count (the voice sheet or the
rulings say so) is no finding.

Clues are no finding. Before you flag a repeat, an oddity or a detail to cut or vary,
check it against llm/habits/reread-hooks.md, the clue register (it lists each chapter's plants;
read it, though you read no notes): a detail listed there is planted on purpose, and is never a finding to cut, vary or explain. Say "clue, kept"
if you noticed it.

Report each finding as:
- quote: the exact text, 25 words at most
- file and line
- whose habit, and the sheet line it breaks or borrows (quoted), or "none recorded"
- why: one sentence
- severity: break, weak, or taste
- direction: one line

Then a short list headed "Drafters' habits": each repeated behavior no sheet records, with
its quotes, for the writer to keep, move or cut.

Do not rewrite the text. Do not praise. Inventing a finding is worse than missing one.
Write it all to runs/habits/report.md, headed "# Critic: habits, 00400", and finish with a one-line tally.
Write your report to runs/habits/report.md. Give every finding as a list item that begins `- line N:` with the line number in the chapter file.
```
