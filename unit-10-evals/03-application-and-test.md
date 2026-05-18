# Unit 10: Evals
## Stage 3: Application

---

### The prompt change that almost shipped broken

A team tweaks their system prompt to improve tone. Quick manual test looks great. Someone runs the eval suite. Accuracy on technical questions dropped from 87% to 61%. The tone fix made the model ignore technical details.

Eval caught it before users did. Without the suite, this ships and nobody knows why technical support tickets spike three days later.

---

### Measuring RAG quality before going live

A company builds RAG over 10,000 internal documents. Before launch, groundedness evals on 500 sample questions show 23% of answers contain at least one fabricated claim. They fix chunking and retrieval threshold. Groundedness goes to 96%. Now they ship.

Without evals, they launch a product that fabricates 1 in 4 answers.

---

### LLM as judge for tone at scale

A brand needs every AI response to sound warm and human. Manual review of 10,000 daily responses is impossible. LLM judge scores every response for warmth 1 to 5, flags anything below 3 for human review.

Automated evals handle 95% of quality control. Humans focus only on edge cases. This is how production AI quality control actually works.

---

## Stage 4: Test

---

### Question 1
Difference between groundedness eval and LLM as judge?

**Kishu's answer:** Groundedness eval checks whether every claim in the output exists in the retrieved RAG documents. Used specifically for RAG systems to catch fabrication. LLM as judge scores quality, tone, completeness, and relevance at scale. Used when output quality is subjective and cannot be checked with exact match.

---

### Question 2
Accuracy score drops from 91% to 74% overnight. No prompt changes. What do you investigate?

**Three causes to check:**
1. Base model update: providers sometimes push silent model updates that change behavior.
2. Knowledge base change: new or modified documents in the RAG system affecting retrieval quality.
3. Infrastructure change: chunking size, retrieval threshold, or embedding model change.

Score drops without prompt changes almost always point to one of these three.

---

### Question 3
Teammate says "we manually test 20 examples before every release, that is good enough." What do you say?

**Kishu's answer:** 20 examples does not cover all modules. A change that fixes one use case can silently break another. Run a full automated eval suite across all major use cases every release. Manual testing 20 examples is a gut check, not a quality gate.

---

### Question 4
Four things to always eval in a customer support bot and how to measure each.

**Kishu's answer:**
- **Accuracy:** LLM as judge or exact match against known correct answers.
- **Groundedness:** check every claim exists in retrieved documents, not fabricated.
- **Tone and format:** LLM as judge scoring warmth, brand voice, and output structure 1 to 5.
- **Safety:** contains check flagging harmful, offensive, or sensitive content before it reaches users.

---

### Score
3.5 out of 4. Unit 10 complete.

---

### The three things to never forget from this unit

1. Evals are not optional. They are the difference between shipping with confidence and shipping with hope.
2. Always run the full suite on every change. Regressions kill products silently.
3. Score drops without prompt changes mean: check model updates, KB changes, and infrastructure changes first.
