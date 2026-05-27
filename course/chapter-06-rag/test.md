# Chapter 6 Test

Answer in your own words. No looking back. Answers at the bottom. Do not scroll until you are done.

---

## Question 1
What are the 3 steps in every RAG system? Describe each in one sentence.

## Question 2
A user asks your HR chatbot: "Can I carry forward unused annual leave?" The chatbot says "I don't have that information." But the answer IS in your employee handbook. What is the most likely reason it failed, and what would fix it?

## Question 3
Your company wants to build an AI assistant that answers questions about your product catalogue. The catalogue has 2,000 products, each with a description, specs, and price. Why would you use RAG for this instead of just putting the entire catalogue in the system prompt?

---
---
---
---
---

## Answers (no peeking)

**Q1:**
1. **Index:** Store your documents (or chunks of them) in a searchable form.
2. **Retrieve:** When a user asks a question, find the document chunks most relevant to that question.
3. **Augment and generate:** Paste the retrieved chunks into the prompt and ask the model to answer from them.

**Q2:** The most likely reason is a vocabulary mismatch in retrieval. The user said "carry forward" but the document probably says "carry over" or "roll over." Keyword search missed the match. The fix is to use semantic search (embedding-based retrieval), which finds documents by meaning rather than exact word match.

**Q3:** Two reasons. First, 2,000 product descriptions would be far too many tokens to fit in a single prompt. Even if they fit, the model would struggle to find the right product in that much noise. Second, the catalogue changes regularly. New products get added, prices change. With RAG you update the document store. With a system prompt you would have to manually rewrite it every time something changes. RAG makes the knowledge base easy to maintain.

---

If you got all three right, move to Chapter 7: Vector Databases.

If Q2 felt hard, reread the deep-dive section on vocabulary mismatch. That gap between what users say and what documents say is the most common reason RAG fails in production.
