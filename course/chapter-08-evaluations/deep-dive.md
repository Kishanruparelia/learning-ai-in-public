# Deep dive: Evaluations at scale

Optional reading. Skip if you just want to use AI. Read if you want to understand it.

---

## Human eval vs LLM eval trade-offs

| | Human eval | LLM eval |
|--|-----------|----------|
| Accuracy | High for nuanced tasks | Good for most tasks, misses subtle context |
| Speed | Slow (hours to days) | Fast (seconds) |
| Cost | High | Low |
| Consistency | Varies between raters | Consistent for the same model and prompt |
| Scale | Hard to scale | Scales easily |

The practical approach most teams use: LLM eval for fast iteration during development, human eval for final quality checks before a major release or for high-stakes domains.

---

## The eval judge is also an LLM and can be wrong

LLM-as-a-judge has known biases:

**Verbosity bias:** Longer answers tend to score higher even when a shorter answer is actually better.

**Self-preference bias:** If you use the same model to generate and judge, it tends to rate its own outputs higher.

**Position bias:** When comparing two options, the judge sometimes favours whichever was presented first.

How to reduce these:
- Use a different, stronger model as the judge than the one generating answers
- Ask the judge to evaluate one answer at a time, not compare two
- Be very specific in your scoring rubric so the judge has clear criteria, not vague ones

---

## Regression testing

Once you have a baseline eval score, regression testing means re-running your full eval set after every change.

The goal: ensure a change that improves one thing does not silently break something else.

This is especially important in RAG systems where changes to chunking, retrieval parameters, or embedding models can have unpredictable effects on downstream answer quality.

A simple version: store your eval results in a spreadsheet or file after each run. Track the score over time. A sudden drop tells you something broke.

---

## Eval-driven development

The most rigorous teams write their eval set before they build the system. Not after.

The process:
1. Define what good looks like. Write 20 to 50 test cases with expected outputs or scoring criteria.
2. Build the first version of the system.
3. Run evals. Get a baseline score. It will be low.
4. Iterate on the system (prompts, retrieval, chunking) with evals running after each change.
5. Ship when the eval score meets your threshold.

This mirrors test-driven development in software engineering. The tests define the target. The code (or in this case, the AI system) has to pass them.

---

## Chunked evaluation for RAG

For RAG systems, split your evaluation into two parts and measure them separately:

**Retrieval eval:**
- For each question, what document should have been retrieved?
- Was that document actually in the top results?
- Metric: recall at K (was the right document in the top K results?)

**Generation eval:**
- Given the correctly retrieved document, did the model generate the right answer?
- Metric: accuracy, LLM-as-a-judge, or exact match depending on the task

This separation tells you where the problem is. If retrieval recall is low, your chunking or embedding is the problem. If generation accuracy is low despite good retrieval, your prompt or model is the problem.

---

## Benchmark datasets vs your own eval set

Public benchmark datasets (MMLU, TruthfulQA, HaluEval, RAGAS) measure general model performance.

They tell you very little about how a model will perform on your specific task.

The only eval that matters for a production AI product is the one built from your actual use case, your actual document collection, and your actual users' questions.

Public benchmarks help you choose a starting model. Your own eval set tells you whether that model actually works for you.

---

## When evals are not worth building

Not every AI feature needs a formal eval set.

If the feature is:
- Low stakes (a nice-to-have, not a core workflow)
- Easy to verify visually (a one-off formatting task)
- Used by very few people

Then manual spot-checking is fine.

Invest in formal evals when:
- The feature is in a critical workflow
- Users will trust the output without checking it
- You are making frequent changes to prompts, models, or data
- Being wrong has real consequences