# Deep dive: Why hallucinations cannot be fully eliminated

Optional reading. Skip if you just want to use AI. Read if you want to understand it.

---

## The root cause

An LLM assigns a probability to every possible next token. It picks one based on those probabilities.

The model was trained to produce fluent, confident, contextually appropriate text. Confident and fluent text gets reinforced. Hedged, uncertain text gets less reinforcement unless the training data specifically included examples of appropriate uncertainty.

The result: the model has no internal signal that distinguishes "I know this for certain" from "I am pattern-matching toward something that sounds right." Both feel the same to the model because there is no "feel." There is only next-token prediction.

This is different from a database, which either has a record or returns null. The model always has a next token.

---

## Why RLHF helps but does not solve it

After pretraining, models go through a process called RLHF (Reinforcement Learning from Human Feedback).

Human raters score model outputs. The model learns to produce outputs that humans rate highly. Humans rate confident, helpful answers highly. Uncertain, hedging answers get lower scores even when the uncertainty is honest.

So RLHF can accidentally train models to sound more confident than they should be. This is an active area of research. Some newer training approaches specifically reward calibrated uncertainty.

---

## What RAG does

RAG stands for Retrieval Augmented Generation. It is the most practical solution to factual hallucinations at scale.

Instead of relying on the model's internal knowledge:
1. Your system retrieves relevant documents from a database based on the user's question.
2. Those documents are pasted into the prompt as context.
3. The model is told to answer only from those documents.

Now the model is not guessing from training data. It is reading real content and summarising it.

This dramatically reduces factual hallucinations because the answer is in the prompt. The model still needs to read and extract accurately, but that is much easier than generating from memory.

We cover RAG in Chapter 6.

---

## Hallucination benchmarks

AI companies publish benchmark scores for their models, including hallucination rates. Common benchmarks include TruthfulQA and HaluEval.

But benchmark scores on standard questions tell you little about hallucination rates on your specific domain.

A model might score 80% on TruthfulQA and still confidently fabricate SEBI circular numbers because SEBI regulations were underrepresented in training data.

The only reliable way to measure hallucination risk for your usecase is to build an evaluation set from your own domain and test it. We cover evaluations in Chapter 8.

---

## The confidence calibration problem

Ideally, when a model says "I'm confident about X", it should be right about X most of the time. When it says "I'm not sure about Y", it should be right less often.

This property is called calibration. Well-calibrated models exist. Most production LLMs are not well calibrated because they were optimised for helpfulness and fluency, not for accurate uncertainty expression.

Practical consequence: do not use the presence or absence of hedging language in a model's output as a reliable signal of accuracy. The model saying "I'm fairly confident" means almost nothing.

---

## High-stakes domains

In medicine, law, and finance, hallucinations are not just embarrassing. They are dangerous.

A hallucinated drug interaction. A fabricated legal precedent. A made-up SEBI exemption.

This is why regulated industries are moving toward architectures that keep the LLM in the "drafting and formatting" role while a retrieval system or human provides the authoritative facts. The model writes clearly. The facts come from verified sources.

That architecture is the practical answer to hallucinations in production systems.
