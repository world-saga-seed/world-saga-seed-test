# Run: voice and mechanism critic

**Model:** Sonnet. The kit's prompt (`plan/workflows/drafting/prompts/voice-mechanism.md`, v3) is a critic, not a Haiku finder.

**How to run:** start a fresh session in this repo's top folder with that model, paste the block below, and let it write its report. It must never see `llm/voice-mechanism/answers.md`. Then score it: `python3 llm/score.py llm/voice-mechanism/answers.md runs/voice-mechanism/report.md`.

**Filled for this book:** `{REPO}` is `book/`, with every path given from the repo's top folder; the chapter is this section's faulted copy. `{JOINS}` is none (no chapter either side is drafted). `{TELLS}` is `tools/tells.py` on the chapter (with the banned list) and on the style sample, saved as [tells.txt](tells.txt) and pasted in; `{RANGES}` is the voice sheet's Texture table. `{SOUNDS}` is none: the book writes no sound spans. `{TOPICS}` is the causeway and tide-table cards. The book has no `plan/reread-hooks.md`; [reread-hooks.md](reread-hooks.md) in this folder is the smallest clue register for 00400, copied from its notes' clue line.

```text
You are a critic for a novel in progress, in the folder book/ (every path below is given
from the repo's top folder). Every file is read-only except your one output file. Run no
git commands. Do not launch agents.

The chapters: llm/voice-mechanism/chapter.md (chapter 00400). For the joins only, also read nothing: no chapter either side of 00400 is drafted.

Read the POV file first: book/story/voice/pov-00400.md if it exists,
else book/story/voice/pov.md.
It sets whose head the narration is in, its distance, what each head may know and what
it never tells. Where it and the voice sheet differ, the POV file wins: judge the chapter
against the narration it chose, never against another.

Read book/story/voice/voice.md and book/story/voice/banned.txt (the rules), the voice sheet of each
head the POV file names, and two or three of the
style samples in book/story/voice/samples/: the writer's own lines, the voice
as the writer set it. Calibrate on them, and never flag a line because it resembles them.
Do not read the outlines or the notes for drafting.

Six questions:

1. Voice. I think these chapters are poorly matched with the voice. Can you tell me where?
   Look for: the narrator explaining the plot or lining up clues for the reader; recycled
   phrases and closers, within these chapters or reused from the joins (none); narration that tells
   a feeling the scene already shows; lines that run long where the narrator would be
   short; comparisons from outside the narrator's life; anything said twice. Kind: voice.

2. Mechanism. Where does the page say how something works that it should only show? Where
   does the narration give a cause the narrator could not know, or stop the scene to
   explain? A local giving the common explanation, or a character giving their own theory
   in their own words, is not a finding. You may read book/world/places/the-causeway.md and
   book/world/things/the-tide-table.md only to recognize a true
   cause when it leaks. Kind: mechanism.

3. Model tells. The numbers are below:

chapter.md                     w=  555 way/k= 0.0 asif/k= 0.0 and/s=0.49 neg/k=12.6 med=11 sd= 9.7 short%= 30 long%= 14 button%= 12

1 banned-word hits:
llm/voice-mechanism/chapter.md:29  sandbar  | I rubbed the whiting off my thumb onto my skirt and walked back slowly. The sandbar off the holm hel

sample-pages.md                w=  226 way/k= 0.0 asif/k= 0.0 and/s=0.94 neg/k=22.1 med= 8 sd=12.2 short%= 35 long%= 18 button%= 25

   The samples' range is the voice sheet's Texture table (book/story/voice/voice.md): and/s
   0.94, way/k 0.0, sd 12.2. Flag, with
   the paragraph's line: the "the way you / the way a" simile running above the range or
   twice in a paragraph; sentences chained with "and" through three or more clauses;
   paragraphs with three or more negations or three or more "looked at"; the stock beats
   ("It was not X. It was Y."; a list of three abstract clauses; the quiet-realization
   paragraph that ends "and then I let it go"; a short summing-up tag line closing a scene).
   The samples use some of each: flag density and stacking above theirs, never a single
   use. Flag a chapter below the range too (chopped, every join cut). Kind: tell.

   Knots. tells.py prints a "knot" line for each narration sentence of 35 words or more
   with a semicolon: flag one that runs two main clauses through it, or turns a corner
   mid-sentence, as weak, direction split; a list held by semicolons is no finding.

   Sound spans. None: this book writes no sound spans, so there is nothing to check here.
   Kind: voice.

4. Hindsight. The book is told as it happens (book/story/voice/voice.md, The rule): flag any line that tells from after the events
   ("later I learned", "I never saw her again"). Kind: voice.

5. Register. Plain by default. Close detail where something holds her: work in skilled
   hands, the lens, the weather turning, Agnes's hands. A line or a gap for what bores her
   (book/story/voice/voice.md, The register). Flag a scene that is flat where
   something should hold the narrator, detail spent evenly on what does not, a dull stretch
   told at length, or comparisons spread evenly instead of gathered where the narrator
   looks hard. Kind: voice.

6. Measures and narrators. Flag a chapter whose sentence-length spread falls below the
   samples' (the rhythm flattening), whose button% runs above theirs, or where a body part
   that "went" or "came" clusters in one stretch: candidates, kind tell, severity taste
   unless they cluster. In a piece with another narrator, flag any stretch where that
   narrator sounds like the main one. Kind: voice.

Clues are no finding. Before you flag a repeat, an oddity or a detail to cut or vary,
check it against llm/voice-mechanism/reread-hooks.md, the clue register (it lists each chapter's plants;
read it, though you read no notes): a detail listed there is planted on purpose, and is never a finding to cut, vary or explain. Say "clue, kept"
if you noticed it.

Held facts. The reader key, book/plan/reader-tests/key.md, lists what the reader must not
get (its hidden and forbidden entries; read it, though you read no outline). A line that
states a held fact, or lets a reader state one, is a break, whoever narrates.

Several heads, or omniscient. Where the POV file gives several heads, judge each section
by its own head's voice sheet and samples, and flag a paragraph whose voice belongs to the
other head. Where it is omniscient, entering a head the POV file allows is no finding; the
question is whether each move into a person or a place is marked (a new paragraph, the
person or place named first), and whether the narrator tells what the POV file says it
never tells.

Start with a short overall voice note (one paragraph). Then each finding as:
- quote: the exact text, 25 words at most
- file and line
- kind: voice, mechanism or tell
- rule: the file and heading it breaks, or "recycled" / "repeat" with the other line
- why: one sentence
- severity: break, weak, or taste
- direction: one line (cut, trim to what, or make plain)

Do not rewrite the text. Do not praise. Inventing a finding is worse than missing one.
Write it all to runs/voice-mechanism/report.md, headed "# Critic: voice and mechanism, 00400", and finish with a
one-line tally.
Write your report to runs/voice-mechanism/report.md. Give every finding as a list item that begins `- line N:` with the line number in the chapter file.
```
