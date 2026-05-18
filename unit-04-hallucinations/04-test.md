# Unit 4: Hallucinations
## Stage 4: Test

---

### Scenario test

A company's AI product has three problems:

1. It invents policy documents and cites them confidently.
2. It ignores the instruction to keep responses under 50 words.
3. Portfolio calculations have correct individual numbers but wrong conclusions.

**Kishu's answers:**

1. Fabrication. Fix: demand citations, allow the model to refuse if unsure.
2. Instruction. Fix: move the rule to the system prompt.
3. Logical. Fix: chain of thought, step by step reasoning.

---

### Score
3 out of 3. Unit 4 complete.

---

### The three things to never forget from this unit

1. Hallucinations are not a bug. They are the natural output of a next word predictor with no live data and no permission to say "I don't know."
2. Each type has a different fix. Calling everything "hallucination" without knowing the type means you cannot choose the right solution.
3. RAG fixes Factual hallucinations. That is why it is the most important concept in production AI. Unit 5 next.
