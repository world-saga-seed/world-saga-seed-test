# Run: setup and belief critic

**Model:** Sonnet. The kit's prompt (`plan/workflows/drafting/prompts/setup-belief.md`, v4) is a critic, not a Haiku finder.

**How to run:** start a fresh session in this repo's top folder with that model, paste the block below, and let it write its report. It must never see `llm/setup-belief/answers.md`. Then score it: `python3 llm/score.py llm/setup-belief/answers.md runs/setup-belief/report.md`.

**Filled for this book:** `{REPO}` is `book/`, with every path given from the repo's top folder; the chapter is this section's faulted copy. `{READ_BEFORE}` is none (00400 is the only drafted chapter). `{TOPICS}` is the book's cards. `{FIRSTUSE}` is `tools/firstuse.py llm/setup-belief/chapter.md --cards book/world`, saved in this folder (the chapter is the book's first, so every card word in it is listed). `{KNOWLEDGE}` is `tools/knowledge.py 00400 --dir book/story/voice/knowledge`, saved in this folder. `{PEOPLE}` is Wren and Agnes; only Wren has a sheet, so Agnes's card is named beside it.

```text
You are a critic for a novel in progress, in the folder book/ (every path below is given
from the repo's top folder). Every file is read-only except your one output file. Run no
git commands. Do not launch agents.

Two questions, on the chapter llm/setup-belief/chapter.md (chapter 00400):

1. Setup. Where does something beyond the characters' ordinary reach (a rescue, a windfall,
   a lucky find, a stranger who hands over exactly what the scene needs, a power or
   authority stepping in) turn up when the story needs it, with no rule in the notes or
   earlier beat that puts it there? Where is a power or resource used once that would solve
   later problems too? Where does a person act from convenience rather than a cause the
   page gives? Judge against the drafts before (none: 00400 is the first chapter of this
   book drafted; skim earlier as needed) and the setting's topic files, the cards in
   book/world/ (each folder has a README index).

   Setting words first on the page. llm/setup-belief/firstuse-00400.md lists the words this chapter is the
   first in the book to use that the cards also use (tools/firstuse.py). For each that
   names a thing, a tool or a step the reader needs (not a plain word), is it set up on
   the page before or here, or plain from context? A word that assumes the reader has
   read the cards is a setup finding; so is "as I had been shown" pointing back to a
   showing no page has.

2. Belief. Given only what each character has lived and believes by this point, where would
   they not do or say this? Where the POV file gives several heads, judge each person's
   inner life only where the narration is in their head; elsewhere, judge only what they
   do and say. A narrating head acts on what its knowledge
   guard says it knows and believes at this chapter (llm/setup-belief/knowledge-00400.md), wrong
   beliefs included: an act that follows a listed wrong belief is not a finding. The characters: Wren Ashby, the narrator
   (book/story/notes/characters/wren.md), and Agnes Rook (no sheet; her card is
   book/world/people/agnes-rook.md). Their sheets are in
   book/story/notes/characters/; what each has lived is in the drafts before.

Do not read this chapter's outline or its notes for drafting: judge the page as a reader
who knows the setting's rules would. Do not read anything later. Judge only setup and
belief; ignore voice, style and facts.

Report each finding as:
- quote: the exact text, 25 words at most
- file and line
- kind: setup, or belief (and whose)
- why: one sentence, citing the rule or the earlier beat
- severity: break, weak, or taste
- direction: one line (for a setup: what rule or earlier beat it would need)

Do not rewrite the text. Do not praise. If you find nothing, say "No findings"; inventing a
finding is worse than missing one. Write the findings to runs/setup-belief/report.md, headed
"# Critic: setup and belief, 00400", numbered, and finish with a one-line tally.
Write your report to runs/setup-belief/report.md. Give every finding as a list item that begins `- line N:` with the line number in the chapter file.
```
