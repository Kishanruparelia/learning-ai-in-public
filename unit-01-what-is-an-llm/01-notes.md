# Unit 1: What is an LLM?

## Stage 1: Concept

---

### The Autocomplete Kid

Imagine a kid who has read every book, every WhatsApp message, every news article, every Reddit post ever written. Billions of pages. The kid never went to school. Never learned rules of grammar formally. Just read, and read, and read.

Now you show this kid the beginning of a sentence:

**"The capital of France is ___"**

The kid does not "know" the answer the way a textbook does. But the kid has seen this pattern so many times that filling in "Paris" feels completely natural. It is the most likely next word based on everything read.

That kid is an LLM.

**LLM stands for Large Language Model.** Large because it trained on a huge amount of text. Language because it works with words. Model because it is a mathematical pattern built from all that reading.

---

### The one thing that explains everything

An LLM does exactly one thing:

> **Given what came before, predict what comes next.**

Word by word. Every single response you get from ChatGPT, Claude, or Llama is just this process running thousands of times in a row.

It does not think. It does not understand. It does not look anything up. It predicts the most plausible continuation based on patterns from training.

This one idea explains everything:
- Why it gets things wrong (predicted a plausible word, not a true one)
- Why it can write poetry (patterns of poems exist in training)
- Why it can code (patterns of code exist in training)
- Why it sounds confident even when wrong (confidence is a pattern too)

---

### The 10,000 people mental model

Think of it like this. There are 10,000 people in a room. You want to find one specific person.

You say: "Find me someone aged 30." Now you are down to 100 people.

You add: "And unmarried." Now you are down to 10.

You add: "And works in a broking team." Now you are down to 1 or 2.

That is exactly what context does to an LLM. Every word you add narrows the prediction down further. More context, more accurate output. The model is not filtering a list. It has seen millions of such patterns during training and learned how context narrows things down.

**Better the context, better the prediction. Remember this line. It is the core principle of prompting and RAG both.**

---

### What is training?

Training is the process where the kid does all that reading.

Engineers feed the model billions of text examples. The model adjusts its internal numbers (called weights) until it gets good at predicting the next word. This runs on thousands of GPUs for weeks and costs millions of dollars.

You never do this as a builder or AI PM. You work with models that are already trained. Think of training like baking a cake. You do not bake it. You buy it from the shop (OpenAI, Anthropic, Meta) and decide what to do with it.

---

### Three things an LLM is NOT

This is as important as knowing what it is.

**Not a search engine.** Google fetches real pages from the internet. An LLM generates text from memory. No live connection to the world unless you build one.

**Not a database.** A database stores facts and retrieves them exactly. An LLM approximates from patterns. Close, but not exact.

**Not a brain.** No feelings, no goals, no awareness. A very sophisticated pattern matcher. Treating it like a brain leads to bad product decisions.

---

### Why this matters for building AI products

Every product decision traces back to this mental model.

"Why does the chatbot give wrong answers?" It predicted a plausible word, not a true one.

"Why does it forget what I said earlier?" It can only see a limited window of text at a time.

"Why is it expensive to run?" Predicting thousands of tokens for thousands of users takes enormous compute.

"Why does more context help?" More context narrows the probability of the next word, just like narrowing from 10,000 people to 1.

---

### Self-check (answer before moving to Stage 2)

1. What does LLM stand for? What does each word mean?
2. What is the one thing an LLM actually does?
3. Name three things an LLM is NOT.
4. Why does more context lead to better output? Use the 10,000 people example.
