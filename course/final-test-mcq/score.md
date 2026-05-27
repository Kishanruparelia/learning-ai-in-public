# Answer Key and Score Sheet

**Do not open this until you have answered all 30 questions.**

---

## Answer Key

| Q | Answer | Chapter |
|---|--------|---------|
| 1 | B | What is an LLM |
| 2 | C | What is an LLM |
| 3 | B | What is an LLM |
| 4 | C | Tokens |
| 5 | B | Tokens |
| 6 | B | Tokens |
| 7 | B | Prompting |
| 8 | C | Prompting |
| 9 | B | Prompting |
| 10 | B | Hallucinations |
| 11 | C | Hallucinations |
| 12 | C | Hallucinations |
| 13 | C | System Prompts |
| 14 | B | System Prompts |
| 15 | B | System Prompts |
| 16 | B | RAG |
| 17 | B | RAG |
| 18 | C | RAG |
| 19 | B | Vector Databases |
| 20 | B | Vector Databases |
| 21 | B | Vector Databases |
| 22 | B | Evaluations |
| 23 | B | Evaluations |
| 24 | C | Evaluations |
| 25 | B | Agents and Tool Use |
| 26 | C | Agents and Tool Use |
| 27 | B | Agents and Tool Use |
| 28 | B | Cost, Latency, Model Selection |
| 29 | B | Cost, Latency, Model Selection |
| 30 | C | Cost, Latency, Model Selection |

---

## Scoring

Count your correct answers. Each correct answer is 1 mark. No negative marking.

| Score | Result | What it means |
|-------|--------|---------------|
| 27 to 30 | Distinction | You have a strong command of all 10 chapters. Ready to build. |
| 21 to 26 | Pass | Solid foundation. Review the chapters where you dropped marks. |
| 15 to 20 | Borderline | Revisit the chapters you struggled with before moving forward. |
| Below 15 | Not yet | Go back through the course. The concepts need more time to settle. |

---

## Chapter-wise breakdown

Use this to see which chapters need review. Count your correct answers per chapter group.

| Chapter | Questions | Your score |
|---------|-----------|------------|
| Ch 1: What is an LLM | Q1, Q2, Q3 | /3 |
| Ch 2: Tokens | Q4, Q5, Q6 | /3 |
| Ch 3: Prompting | Q7, Q8, Q9 | /3 |
| Ch 4: Hallucinations | Q10, Q11, Q12 | /3 |
| Ch 5: System Prompts | Q13, Q14, Q15 | /3 |
| Ch 6: RAG | Q16, Q17, Q18 | /3 |
| Ch 7: Vector Databases | Q19, Q20, Q21 | /3 |
| Ch 8: Evaluations | Q22, Q23, Q24 | /3 |
| Ch 9: Agents and Tool Use | Q25, Q26, Q27 | /3 |
| Ch 10: Cost, Latency, Model Selection | Q28, Q29, Q30 | /3 |
| **Total** | | **/30** |

---

## Explanations for commonly missed questions

**Q4 (Tokens - word count):**
200 words x 1.3 tokens per word = 260 tokens. The 1.3 multiplier is the standard rule of thumb.

**Q9 (Chain of thought):**
The model generates one token at a time. Each token is influenced by everything before it. When you force intermediate reasoning steps, those steps become context that shapes the final answer. The model is not "thinking harder." It is using its own written-out steps as a scaffold.

**Q15 (System prompt cost):**
The system prompt is included in every single API call, not just the first one. A 400-token system prompt across a 20-turn conversation adds 8,000 tokens in system prompt alone. Multiplied by thousands of users, this becomes significant.

**Q20 (Embedding model switch):**
Each embedding model maps text to a different vector space. Vectors from Model A and Model B are not comparable. Searching with a Model B query against Model A document vectors is like searching a French dictionary with an English word. You must re-embed everything.

**Q26 (Agent reliability):**
0.9 to the power of 10 = 0.349, approximately 35%. This is one of the most important numbers in agent design. Long chains of steps with individually high accuracy still produce unreliable end-to-end results.

---

## What next

If you passed: go build the capstone project in `capstone-project/README.md`.

If you did not pass: go back to the chapters where you scored below 2 out of 3. Re-read the README and try the practical again. Then retake the test.

The goal is not the score. The goal is that the concepts are clear enough to use when you are building something real.
