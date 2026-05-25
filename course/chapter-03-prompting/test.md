# Chapter 3 Test

Answer in your own words. No looking back. Answers at the bottom. Do not scroll until you are done.

---

## Question 1
Name the 4 prompting patterns from this chapter. One sentence on each.

## Question 2
Here is a weak prompt. Rewrite it using at least 2 of the 4 patterns:

**Weak prompt:** "Write a message to a client about their portfolio."

## Question 3
A colleague says: "I tried chain of thought but the model still got the maths wrong." What is one thing they could check or try?

---
---
---
---
---

## Answers (no peeking)

**Q1:**
- **Role + Task + Format:** Give the model a persona, a specific task, and tell it exactly what shape the output should be.
- **Few-shot examples:** Show one or more examples of what good output looks like before asking for the real thing.
- **Chain of thought:** Tell the model to work through the problem step by step before giving the final answer.
- **Constraints:** Tell the model what to avoid, what length to use, and what rules to follow.

**Q2:** There is no single right answer. A strong rewrite would include at least a role ("You are a relationship manager"), a specific task ("write a WhatsApp message to client Priya"), and at least one constraint ("maximum 3 sentences, end with a call to action"). If you added a tone example or format instruction, even better.

**Q3:** Check whether the steps in the chain of thought were specific enough. Saying "think step by step" is a hint, but listing the exact steps (calculate Fund A profit, calculate Fund B profit, add them, divide by total) leaves less room for the model to skip a step. Also check if temperature is too high, which can introduce randomness into calculations.

---

If you got all three right, move to Chapter 4: Hallucinations.

If Q2 felt hard, go back and reread the "combining the patterns" section in README.md. That is the most important practical skill in this chapter.
