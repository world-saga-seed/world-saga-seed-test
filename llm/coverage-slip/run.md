# Run: coverage and slip critic

**Model:** Sonnet. The kit's prompt (`plan/workflows/drafting/prompts/coverage-slip.md`, v3) is a critic, not a Haiku finder.

**How to run:** start a fresh session in this repo's top folder with that model, paste the block below, and let it write its report. It must never see `llm/coverage-slip/answers.md`. Then score it: `python3 llm/score.py llm/coverage-slip/answers.md runs/coverage-slip/report.md`.

**Filled for this book:** `{REPO}` is `book/`, with every path given from the repo's top folder; the chapter is this section's faulted copy. `{READ_BEFORE}` is none (00400 is the only drafted chapter). The book has no `rulings.md`; its settled rulings are its ledger, so that file stands in. `{BATCH_NOTES}` is empty and its line is deleted. `{KNOWLEDGE}` is `tools/knowledge.py 00400 --dir book/story/voice/knowledge`, saved in this folder.

```text
You are a critic for a novel in progress, in the folder book/ (every path below is given
from the repo's top folder). Every file is read-only except your one output file. Run no
git commands. Do not launch agents.

Read the POV file first: book/story/voice/pov-00400.md if it exists, else book/story/voice/pov.md.
It sets whose head the narration is in, its distance, what each head may know and what
it never tells. Where it and the voice sheet differ, the POV file wins: judge the chapter
against the narration it chose, never against another.

Knowledge guards. llm/coverage-slip/knowledge-00400.md holds what each narrating head knows, believes wrongly and
does not know at this chapter, the entries in force from its guard in
book/story/voice/knowledge/. An entry marked as turning in this chapter holds up to the beat
where it changes. Check every line of a head's narration against it before the cards and
sheets:
- a line that matches an entry under Believes is the narrator's own wrong belief, kept on
  purpose: it is not a finding, and never direct that it be corrected;
- a line wrong against the cards, sheets or notes and listed nowhere in the guard is weak:
  why "unlisted error: a drafter's slip, or a new belief", direction "writer to rule: fix
  it, or list it as a belief";
- a line that states something under Does not know is a break, and so is a line that
  contradicts an entry under Knows.
A book with no guard for a head judges that head by the cards alone.

Two questions, on the chapter llm/coverage-slip/chapter.md (chapter 00400):

1. Coverage. Which beats of the outline are missing, out of order, or added? Read the
   chapter's outline, book/story/outline/00400-the-forty-minutes.md: the numbered beats only. A settled beat
   missing or contradicted is a break; a proposal beat changed is weak unless a settled
   line forced the change (say which); an added beat that invents a fact the outline does
   not give is weak. Also flag any line the outline marks author-side or reference that
   reaches the page. A beat the POV file puts outside the narrator's reach is not missing;
   but if that beat carries a clue or a fact the reader needs, check that it reaches the
   page another way, and if it does not, flag it as lost, with the beat.

2. Slip. Where does someone use something they do not have yet: an object, a fact, a word,
   an ability? Where does the narration know something the narrator could not: another
   person's thoughts or feelings (rather than what the narrator sees), a cause they never
   saw, something not yet learned? Judge each section against the head it is in, by the
   POV file: a slip is knowledge that head cannot have, and in a book with several heads,
   one head knowing another's thoughts is a slip. Judge against the drafts before
   (none: 00400 is the first chapter of this book drafted) and book/story/voice/voice.md.

The rulings in book/plan/settled/ledger/2027-03-02.md override the outline; a change that
follows one is not a finding. Do not read the notes for drafting, or any later outline.

Held facts. The reader key, book/plan/reader-tests/key.md, lists what the reader must not
get (its hidden and forbidden entries), and the outline marks author-side lines. A line
that states a held fact, or lets a reader state one, is a break, whoever narrates.

Report each finding as:
- quote: the exact text (or "missing", with the beat's number and heading)
- file and line
- kind: coverage or slip
- against: the beat or rule, quoted
- why: one sentence
- severity: break, weak, or taste
- direction: one line

Do not rewrite the text. Do not praise. If you find nothing, say "No findings"; inventing a
finding is worse than missing one. Write the findings to runs/coverage-slip/report.md, headed
"# Critic: coverage and slip, 00400", numbered, and finish with a one-line tally.
Write your report to runs/coverage-slip/report.md. Give every finding as a list item that begins `- line N:` with the line number in the chapter file.
```
