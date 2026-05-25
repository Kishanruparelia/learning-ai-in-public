# Chapter 5 Test

Answer in your own words. No looking back. Answers at the bottom. Do not scroll until you are done.

---

## Question 1
What are the 5 things that belong in a system prompt? Name them without looking.

## Question 2
Your colleague puts this rule in every user message they send:
"Always reply in bullet points and keep it under 3 sentences."
What is wrong with this approach, and where should it go instead?

## Question 3
You are building an AI tool for SBI Securities compliance team. A user pastes in a trade note and asks the AI to flag any suspicious patterns. What is one system prompt guardrail you would include, and why?

---
---
---
---
---

## Answers (no peeking)

**Q1:**
1. Persona (who the model is)
2. Scope (what it can and cannot talk about)
3. Rules and guardrails (what it must always or never do)
4. Output format (how replies should be structured)
5. Background context (information about the product, company, or environment)

**Q2:** Putting a permanent formatting rule in the user message means it has to be repeated every single time. If anyone forgets to include it, the output changes. It also adds tokens to every user message unnecessarily. Formatting rules that apply to all conversations belong in the system prompt, where they persist automatically across every turn.

**Q3:** Many valid answers. One strong example: "Never make a definitive compliance ruling. Always end your analysis with: this is an AI-assisted preliminary review and must be reviewed by a qualified compliance officer before any action is taken." The reason: AI can flag patterns but cannot be the final authority on compliance decisions. The guardrail ensures the tool is used as a first-pass filter, not a replacement for human judgment.

---

If you got all three right, move to Chapter 6: RAG (Retrieval Augmented Generation).

If Q3 felt hard, reread the real example section in README.md. Building guardrails for regulated industries is one of the most important skills for an AI PM in fintech.
