# Critic: facts, 00400

*Run 2027-03-03. Facts critic, prompt v1 ([the prompt](../../plan/workflows/drafting/prompts/facts.md)). Fresh agent; read only the chapter, its notes, the settled lines of its outline, and the cards it links. The supervisor's verification is at the end.*

1. **The causeway's hours**
   - quote: The causeway was bare for two hours at every low water, never more
   - file and line: story/prose/00400-the-forty-minutes.md:27
   - against: "It is bare for about four hours at each low water and covered for the rest." (world/places/the-causeway.md, What it is)
   - why: the page halves the crossing time the card settles, and 00700's timing rests on the card.
   - severity: break
   - direction: change to about four hours, or make it "two hours left" for this tide only.

2. **The books in the house**
   - quote: it was the only book in the house besides the log and the Bible
   - file and line: story/prose/00400-the-forty-minutes.md:17
   - against: "It sits on the shelf in the lamp room beside the Board's printed Instructions to Keepers." (world/things/the-log-book.md, What it is)
   - why: the Instructions are a printed book in the house too.
   - severity: weak
   - direction: "the only book in the house that was not the Board's", or leave it as Wren's way of counting.

3. **The cleaning day**
   - quote: the lens was cleaned every Sunday
   - file and line: story/prose/00400-the-forty-minutes.md:3
   - against: "Opens on the day: the first dry morning of March, when the lens is cleaned." (story/outline/00400-the-forty-minutes.md, 1)
   - why: the day of cleaning contradicts the outline.
   - severity: break
   - direction: follow the outline.

Tally: 2 breaks, 1 weak.

## Verification (the supervisor)

`python3 tools/quotes.py reports/critic-facts-00400.md --in reports/snapshot/00400-the-forty-minutes.md` (draft 1, the text the critic read) reports 2 of 3 quotes resolving. Finding 3's quote is not in the chapter: the page says "the first dry morning of the month", which agrees with the outline. **Finding 3 is dropped.** One drop in three is noted against this critic's precision in [plan/state.md](../plan/state.md#critic-calibration).

## To the writer

| # | Finding | Recommendation |
|---|---|---|
| 1 | two hours against four | Fix the page to the card: "bare for about four hours". The card is settled (R0302-07); logged as drift until the redraft. |
| 2 | the Board's Instructions | Leave it. Wren would not count the Board's book as a book of the house; it is her voice, not a fact slip. *(Resolved by judgment, overturnable.)* |
