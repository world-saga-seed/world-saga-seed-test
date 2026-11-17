# Key: inference finder

*Never give this file to the model under test.* The input is [chapter.md](chapter.md): 00400 of *The Tide Clock* (draft 2), with five first-person claims planted that have no grounds on the page, and an invented afternoon added after the original ending (line 31) to give the plants room. Every plant is a whole sentence the original draft does not have; nothing in book/ supports it.

| ID | Line | Kind | Plant | Must |
|---|---|---|---|---|
| K1 | 23 | inside as fact | "Mrs. Rook hated reading the almanac out, and she was ashamed of it." Another's feeling, no sign shown; her card has her read every tide aloud "for thirty years without thinking" (book/world/people/agnes-rook.md, Habits) | `hated\|ashamed` |
| K2 | 37 | verdict, motive | "She had sent me to the post to be rid of my questions, and she did not want to know what the weed said." Why she did a thing and what she wants, nothing seen; the POV file gives Wren no reach into the lamp room while she is away (book/story/voice/pov.md, Witness reach) | `rid of\|my questions\|did not want` |
| K3 | 43 | verdict, past and trade | "Dell had fished out of Saltby before the Board gave him the oil, and he had lost a brother on the sands below the holm." A person's past and trade, told by no one on the page; nothing in book/ gives Dell a past | `Dell\|fished\|brother` |
| K4 | 49 | inside as fact | "She was thinking of her husband, as she always did when the tide turned." Another's thought and habit as fact; watching the water (line 47) does not carry it | `husband\|thinking` |
| K5 | 55 | verdict, cause | "The gallery rail was green at every joint, because the Board had sent cheap brass the year the gallery was built." A cause and a past from before Wren was born; no one tells her | `brass\|gallery was built\|Board` |

**Pass:** 4 of 5 caught.

The Must column (a regex the finding's text must hold) keeps a finding on another claim in the same line, such as line 23's grandmother, from scoring as the catch. The finder lists every inference, about 25 a chapter, so findings away from the plants are expected and not capped. They are not scored as inventions.

## Grounded near misses

Each is an inference grounded on the line before it. The finder should list it **with** that evidence. Listing it with "none on the page" is an error (the section's score.py counts it).

| ID | Line | Grounded by | Claim |
|---|---|---|---|
| N1 | 17 | line 15: `"Mind your ring," she said, sharp, and she shut the almanac on her thumb.` | "She was cross with me for asking": a feeling read from a sharp word and a shut book |
| N2 | 29 | line 27: `"Look and come back," she said. "Do not stand about."` | "I stood and looked at it longer than she would have liked": what Agnes wants, from what she said (the same line's "which meant the water had only just gone off it" is known from 00300, the knowledge guard's Knows) |

## Not breaks, for the judge downstream

Line 57, "because my hand was better", is Wren's listed wrong belief (book/story/voice/knowledge/wren.md, Believes 1), known from 00100. A finder may list it; a judge must pass it.

## Lines verified

```text
$ grep -n "hated reading\|rid of my questions\|fished out of\|thinking of her husband\|cheap brass" chapter.md | cut -c1-60
23:My grandmother had done the same at the end. She had tied
37:She had sent me to the post to be rid of my questions, an
43:After we ate I scoured the oil cans by the door, for Dell
49:She was thinking of her husband, as she always did when t
55:The gallery rail was green at every joint, because the Bo
$ grep -n "sharp, and she shut\|cross with me\|Do not stand about\|would have liked" chapter.md | cut -c1-60
15:"Mind your ring," she said, sharp, and she shut the alman
17:She was cross with me for asking, so I minded it. The alm
27:When the sun was over the chimney she sent me down the ca
29:The causeway was bare for about four hours at each low wa
```
