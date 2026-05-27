# Chapter 7 Test

Answer in your own words. No looking back. Answers at the bottom. Do not scroll until you are done.

---

## Question 1
What is a vector embedding, and what does it mean for two pieces of text to have similar embeddings?

## Question 2
A user types "I need to cancel my subscription." Your knowledge base has an article titled "How to terminate your account." Keyword search returns nothing. Semantic search returns it correctly. Why?

## Question 3
Your team built a RAG system 6 months ago using Embedding Model A. The team wants to switch to a newer, better Embedding Model B. What must they do before the system will work correctly again, and why?

---
---
---
---
---

## Answers (no peeking)

**Q1:** A vector embedding is a list of numbers that represents the meaning of a piece of text. Two pieces of text have similar embeddings when those lists of numbers are close to each other, which happens when the texts carry similar meaning, even if the words are completely different.

**Q2:** Keyword search looks for exact word matches. "Cancel" and "subscription" do not appear in the article title "How to terminate your account," so keyword search finds nothing. Semantic search converts both the query and the article to vectors and measures meaning similarity. "Cancel subscription" and "terminate account" are semantically close, so the article scores high and gets retrieved.

**Q3:** They must re-embed all documents in their knowledge base using Model B. Each embedding model operates in its own vector space. Vectors from Model A and vectors from Model B are not comparable. If they query with Model B but the stored vectors were made by Model A, the similarity scores will be meaningless and retrieval will fail or return random results.

---

If you got all three right, move to Chapter 8: Evaluations.

If Q3 surprised you, reread the "embedding model must stay consistent" section in deep-dive.md. This is a real operational risk in production AI systems that teams regularly underestimate.
