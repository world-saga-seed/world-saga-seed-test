# Verified findings, 00400 (test copy)

*The supervisor's merged list, after verification, for the reviser. Lines point at llm/reviser/chapter.md as given (the run copies it to runs/reviser/ first).*

1. **Hindsight**
   - quote: I did not know yet that the almanac was wrong for the holm.
   - file and line: chapter.md:17
   - rule: book/story/voice/voice.md, The rule ("Told as it happens: no "later I learned", no "I did not know yet"") and "Nothing in the narration says why the tide runs late."
   - severity: break
   - direction: cut the sentence.

2. **A banned phrase**
   - quote: I realized the whiting had dried white in the cuts of the glass
   - file and line: chapter.md:23
   - rule: book/story/voice/banned.txt ("I realized")
   - severity: weak
   - direction: give the whiting drying as she sees it, without "I realized".

3. **The causeway's hours**
   - quote: The causeway was bare for two hours at every low water, never more
   - file and line: chapter.md:27
   - against: "It is bare for about four hours at each low water and covered for the rest." (book/world/places/the-causeway.md, What it is; R0302-07)
   - severity: break
   - direction: about four hours at each low water.

4. **The clue lined up for the reader**
   - quote: By the almanac, low water had been an hour ago. By the weed, it had been no time at all.
   - file and line: chapter.md:27
   - rule: book/story/voice/voice.md, The rule (Wren notices; she does not explain)
   - severity: weak
   - direction: cut the echo, "By the weed, it had been no time at all." Keep "By the almanac, low water had been an hour ago." exactly: it is a clue line (book/story/notes/00400-the-forty-minutes.md, Clues).
