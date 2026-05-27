# Chapter 8 Test

Answer in your own words. No looking back. Answers at the bottom. Do not scroll until you are done.

---

## Question 1
What is an eval set and what 3 types of examples should it include?

## Question 2
Your team changed the system prompt for your AI support tool. The replies feel better to you personally. Is that enough evidence to ship the change? What should you do instead?

## Question 3
You are building a RAG-based FAQ tool. Users report that some answers are wrong. How would you use evaluations to figure out whether the problem is in retrieval or in generation?

---
---
---
---
---

## Answers (no peeking)

**Q1:** An eval set is a collection of test cases used to measure how well an AI system performs. It should include: typical cases (the most common inputs you expect), edge cases (unusual or extreme inputs), and known failure cases (inputs where the model tends to go wrong).

**Q2:** No. Personal impression is not reliable evidence. Prompts that feel better to the person who wrote them often perform worse on the full range of real inputs. You should run your eval set against both the old and new prompt and compare the scores. Only ship if the score improves or stays the same across all dimensions.

**Q3:** Split the evaluation into two independent parts. First, run a retrieval eval: for each test question, manually check whether the correct document was actually retrieved and in the top results. If retrieval recall is low, the problem is in your chunking, embedding model, or search. Second, for the questions where the right document was retrieved, check whether the generated answer was still wrong. If it was, the problem is in your prompt or model. This separation tells you exactly where to focus your fixes.

---

If you got all three right, move to Chapter 9: Agents and Tool Use.

If Q3 felt hard, reread the "chunked evaluation for RAG" section in deep-dive.md. Knowing how to diagnose failures systematically is what makes an AI PM effective beyond the prototype stage.
