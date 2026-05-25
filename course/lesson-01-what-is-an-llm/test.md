# Lesson 1 Test

Answer these in your own words. No looking back at the lesson. Answers are at the bottom, hidden. Do not scroll until you have written your answers.

---

## Question 1
In one sentence, what does an LLM actually do?

## Question 2
Your friend says: "ChatGPT knows everything because it has the internet stored inside it." What is wrong with this statement?

## Question 3
You ask an LLM the same question twice and get two different answers. What is the setting that controls this, and what value would make the answers identical?

---
---
---
---
---

## Answers (no peeking)

**Q1:** An LLM predicts the next word in a sequence, one word at a time, based on patterns it learned from massive amounts of text.

**Q2:** The internet is not "stored" inside the model. The model learned patterns from internet text during training, but it does not look anything up. It generates text that statistically fits the pattern. That is why it can be wrong even about basic facts.

**Q3:** The setting is called **temperature**. Setting `temperature=0` makes the answers identical because the model will always pick the highest-probability next word with no randomness.

---

If you got all three right, move to Lesson 2: Tokens.

If you got any wrong, reread the section in `README.md` that covers it. Then move on.
