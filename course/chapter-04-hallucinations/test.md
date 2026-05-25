# Chapter 4 Test

Answer in your own words. No looking back. Answers at the bottom. Do not scroll until you are done.

---

## Question 1
What is a hallucination? Why is it more dangerous than the AI saying "I don't know"?

## Question 2
Match each hallucination type to its fix:

| Type | Fix |
|------|-----|
| Factual | ? |
| Fabrication | ? |
| Instruction | ? |
| Context | ? |
| Logical | ? |

## Question 3
Your team is building an AI tool that reads client call transcripts and extracts the client's complaint category. Is this high, medium, or low hallucination risk? What one thing would you do to reduce the risk?

---
---
---
---
---

## Answers (no peeking)

**Q1:** A hallucination is when the AI generates output that is confident, fluent, and wrong. It is more dangerous than "I don't know" because the reader has no signal that the information is wrong. A wrong answer that sounds certain gets acted on. A clear admission of uncertainty gets verified.

**Q2:**
| Type | Fix |
|------|-----|
| Factual | Tell it to say "I don't know" if uncertain. Do not ask for data it cannot have. |
| Fabrication | Tell it not to invent. Ask it to say where to look instead. |
| Instruction | Move critical rules to the system prompt, not buried in the user message. |
| Context | Tell it to use only the provided information and quote exact figures. |
| Logical | Chain of thought. List every step it must take before the final answer. |

**Q3:** Medium risk. The model is reading a document you provided (lower risk than pure memory tasks) but it still needs to classify correctly and not add categories that were not in the transcript. The one thing to do: provide a fixed list of allowed categories in the prompt and show one example of correct classification (few-shot). This constrains the output space and reduces both fabrication and instruction hallucination risk.

---

If you got all three right, move to Chapter 5: System Prompts.

If Q3 felt hard, reread the risk spectrum section in README.md. Knowing which tasks need guardrails is the skill that separates a demo from a production product.
