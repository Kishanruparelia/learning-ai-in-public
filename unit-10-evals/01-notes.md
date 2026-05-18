# Unit 10: Evals (Evaluations)

## Stage 1: Concept

---

### The problem nobody talks about

You ship an AI feature. It seems to work. Three weeks later users complain. Answers feel worse. Something changed but nobody knows what. You have no idea because you never measured anything.

This is the most common failure mode in AI product teams. Completely avoidable.

Evals are how you measure whether your AI is actually working.

---

### What is an eval?

A test suite for your AI system. Three parts:

**Input:** a question or prompt you send to the model.
**Expected output:** what a good answer looks like.
**Scoring function:** how close the actual output is to expected.

Run your eval suite before and after every change. Scores drop = something broke. Scores improve = change worked.

---

### Four types of evals

**1. Exact match.** Output must match expected exactly. Works for classification labels, JSON fields, yes or no answers.

**2. Contains check.** Output must contain certain keywords or phrases. Less strict than exact match.

**3. Groundedness check.** For RAG systems specifically. Does every claim in the response exist in the retrieved documents? If not, the model fabricated it. This is the eval type for catching context hallucinations in RAG.

**4. LLM as judge.** Send output to another LLM, ask it to score quality 1 to 5. Evaluates accuracy, tone, completeness, relevance. Most powerful and most widely used in production today.

**5. Human eval.** A human reviews and scores. Most accurate, slowest, most expensive. Used for high-stakes decisions or to validate automated evals.

---

### What to always eval

**Accuracy:** is the answer factually correct?
**Groundedness:** for RAG, is the answer based on retrieved documents or fabricated?
**Tone and format:** does output match brand voice and required format?
**Safety:** does output avoid harmful or sensitive content?

---

### The regression trap

You fix prompt for use case A. Ship it. Three days later use case B is broken. Your change that fixed A accidentally broke B. You never tested B.

This is a regression. Fix: run the full eval suite across all major use cases every time you make any change. Not just the one you were working on.

---

### The one thing that separates toy projects from real products

Any team can build an AI demo that works with perfect inputs in a controlled setting.

A real product works reliably across thousands of real users with messy, unpredictable inputs. The only way to know if yours does is to measure it systematically.

Evals are not optional. They are the difference between shipping with confidence and shipping with hope.

---

### Self check

1. What is an eval and why does every AI product need one?
2. Your RAG bot gives a confident answer not in any retrieved document. Which eval type catches this?
3. You improve your chatbot for billing questions. Before shipping, what do you run?

**Answers:**
1. A test suite measuring AI output against expected output. Needed because AI output is not deterministic and you cannot know if a change broke something without systematic measurement.
2. Groundedness check. Measures whether every claim in the response exists in the retrieved documents. LLM as judge can also catch it but groundedness is the precise term for RAG systems.
3. The full eval suite across all use cases, not just billing. To catch regressions before they reach users.
