# Unit 4: Hallucinations
## Stage 3: Application

Three real product scenarios where hallucinations destroy trust.

---

### The legal and compliance trap

Any AI product that generates or summarizes policy, regulation, or legal content is a Fabrication hallucination waiting to happen. The model generates plausible-sounding circular numbers, clause references, and policy names with complete confidence.

Fix: never let the model generate compliance content from memory. Always ground it in actual documents using RAG. Add a constraint: "if you cannot find this in the provided documents, say so explicitly."

---

### The customer trust problem

A customer asks an AI support bot about their account balance or transaction history. The bot gives a confident number pulled from training patterns, not from the actual database. Customer makes a decision based on wrong information.

This is a Factual hallucination in a high-stakes context. One wrong answer here destroys trust that took years to build.

Fix: never let AI answer questions about live, user-specific data from memory. Always retrieve the actual data first, then let the model respond using only that data.

---

### The silent math error

An AI tool generates a report with calculations. Individual numbers are correct but the percentage change, the growth rate, the comparison logic is wrong. No one catches it because the output looks professional and confident.

This is a Logical hallucination. Dangerous because it is hard to spot without checking the math manually.

Fix: for any calculation, force chain of thought. Better still, do not let the model do the math at all. Use a calculator tool and let the model only interpret the result.
