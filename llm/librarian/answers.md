# Key: librarian

*Never give this file to the model under test.* The questions are [questions.md](questions.md). Six are answered in book/'s notes; two are not, and the right answer to those is "Not in the notes". Paths are inside book/. The **Must hold** column is what score.py checks in each answer (every pattern, case ignored; "|" separates alternatives).

| Q | Answer | File:line | Mark | Must hold |
|---|---|---|---|---|
| 1 | thirty-one years | world/people/agnes-rook.md:7 | Settled R0302-01 | `thirty-one\|31` ; `agnes-rook` |
| 2 | about four hours | world/places/the-causeway.md:7 | Settled R0302-07 | `four hours\|4 hours` ; `the-causeway` |
| 3 | three posts; the third shows it | world/places/the-causeway.md:8 | Settled R0302-07 | `three\|\b3\b` ; `third` ; `the-causeway` |
| 4 | Dell, each January, with the oil | world/things/the-tide-table.md:7 | Settled R0302-06 | `Dell` ; `January` ; `the-tide-table` |
| 5 | rubs it on her skirt; a proposal | story/notes/characters/wren.md:27 | Proposal, from the writer's existing scene | `skirt` ; `proposal` ; `characters/wren` |
| 6 | on the shelf in the lamp room, beside the Board's printed Instructions to Keepers | world/things/the-log-book.md:7 | Settled R0302-08 | `lamp room` ; `Instructions` ; `the-log-book` |
| 7 | Not in the notes: the inspector is never named (closest: world/things/the-log-book.md, Why it matters) | none | | `not in the notes` |
| 8 | Not in the notes: the cards say Agnes adds it and why the water runs late, never who found it (closest: world/places/the-causeway.md or world/people/agnes-rook.md); the reader-test key, outside the notes, lists it as unknown (plan/reader-tests/key.md, K5) | none | | `not in the notes` |

**Pass:** 7 of 8 right, and both not-in-the-notes answers right.

The traps: 5 asks for the mark, and the line is a proposal; 8 tempts "Agnes" (she "has added it for thirty years") or "her husband". An answer to 7 or 8 that says "not in the notes" but then guesses a name still passes the script; read it.

## Lines verified

```text
$ grep -n "thirty-one years" world/people/agnes-rook.md
7:- **Who.** *(Settled R0302-01.)* Keeper of the Skerry Holm light for thirty-one years; ...
$ grep -n "about four hours\|Three tarred posts" world/places/the-causeway.md
7:- **What it is.** *(Settled R0302-07.)* ... It is bare for about four hours at each low water ...
8:- **The posts.** *(Settled R0302-07.)* Three tarred posts mark the way. The weed on the third post ...
$ grep -n "January" world/things/the-tide-table.md
7:- **What it is.** *(Settled R0302-06.)* ... Dell brings the new one each January with the oil.
$ grep -n "skirt" story/notes/characters/wren.md
8:- Habits: thumb on her skirt; checks the weed. ([Habits](#habits))
27:- *(Proposal, from the writer's existing scene.)* Gets oil or soot on her thumb and rubs it on her skirt.
$ grep -n "beside the Board" world/things/the-log-book.md
7:- **What it is.** *(Settled R0302-08.)* ... It sits on the shelf in the lamp room beside the Board's printed Instructions to Keepers.
$ grep -rn -i "inspector" world story/notes | grep -i "name\|Mr\.\|called"   # nothing: the inspector is never named
$ grep -rn -i "first found" world story/notes                # nothing
```
