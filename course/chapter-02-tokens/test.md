# Chapter 2 Test

Answer in your own words. No looking back. Answers at the bottom. Do not scroll until you are done.

---

## Question 1
Is a token the same as a word? Give one example of a word that is more than one token.

## Question 2
You are building an AI tool. Your system prompt is 300 words, the average user message is 40 words, and the average AI reply is 80 words. Roughly how many tokens does one conversation use? (Use the 1.3x rule.)

## Question 3
A user reports that your chatbot "forgot" something they told it 2 hours ago in the same conversation. What most likely happened, and what is the technical name for the limit that caused it?

---
---
---
---
---

## Answers (no peeking)

**Q1:** No. A token is roughly 4 characters or 0.75 words. Long or rare words split into multiple tokens. Example: "Hallucination" is 3 tokens. "Unconstitutional" is 5 tokens. Any similar example is correct.

**Q2:**
- System prompt: 300 x 1.3 = 390 tokens
- User message: 40 x 1.3 = 52 tokens
- AI reply: 80 x 1.3 = 104 tokens
- Total: roughly 546 tokens per conversation

**Q3:** The conversation history grew longer than the model's context window. Once the limit was hit, the oldest messages were dropped and the model no longer had access to what was said earlier. The technical name for this limit is the **context window**.

---

If you got all three right, move to Chapter 3: Prompting.

If you got Q2 wrong, reread the cost section in README.md. The estimation skill matters when you are building real products.
