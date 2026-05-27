# Chapter 7: Vector Databases

**Time needed:** 1 hour
**You will need:** A browser, your Groq API key, Google Colab open

---

## What you will be able to do by the end

1. Explain what a vector is and why it represents meaning
2. Understand how similarity search works
3. Build a semantic search system that finds documents by meaning, not keywords
4. Know where vector databases fit in a production AI system

---

## The big idea

In Chapter 6 you built a RAG system that used keyword matching to find documents. It broke when the user used different words than the document.

Vector databases fix this. They store meaning, not just words. When you search, you search by what you meant, not what you typed.

This is the technology behind every modern search experience that feels like it actually understands you.

---

## What is a vector

A vector is a list of numbers. That is it.

The interesting part is what those numbers represent. When you pass a piece of text through an embedding model, it converts the text into a list of numbers where similar-meaning text produces similar-looking numbers.

Think of it like a map. Every sentence gets a location on the map. Sentences that mean similar things end up close to each other. Sentences about completely different topics end up far apart.

A real embedding vector for a sentence might have 384 or 1536 numbers. You never read those numbers directly. You just use them to measure distance.

---

## How similarity works

Given two vectors, you can calculate how similar they are using a formula called cosine similarity.

The result is a number between 0 and 1:
- **1.0** means identical meaning
- **0.8+** means very similar
- **0.5** means loosely related
- **0.0** means completely unrelated

Examples of what high similarity looks like:

| Text A | Text B | Similarity |
|--------|--------|------------|
| "How do I reset my password?" | "Steps to change my login credentials" | ~0.91 |
| "What is the refund policy?" | "Can I get my money back?" | ~0.88 |
| "Company holiday schedule" | "Best pizza restaurants nearby" | ~0.04 |

The model never saw these pairs during embedding. The similarity emerges from the meaning of the words, not explicit rules.

---

## What a vector database does

A regular database stores rows of data and finds them by matching values exactly.

A vector database stores embeddings and finds them by measuring distance. When you send a query, it converts your query to a vector and returns the stored vectors that are closest to it.

This is called approximate nearest neighbour search, and it is optimised to run over millions of vectors in milliseconds.

Popular vector databases: Chroma, Pinecone, Weaviate, Qdrant, Milvus, and pgvector for PostgreSQL.

In this chapter you will use Chroma, which runs entirely in memory and needs no setup.

---

## The full picture: embedding model + vector database

Two separate components work together:

**Embedding model:** Converts text to vectors. Examples: OpenAI's text-embedding-3-small, Sentence Transformers (free, open source), Cohere Embed.

**Vector database:** Stores those vectors and runs similarity search over them.

You use the same embedding model for both indexing and querying. If you embed documents with Model A and query with Model B, the vectors will be in different spaces and similarity will be meaningless.

---

## Where this fits in the RAG pipeline

In Chapter 6, Step 2 was "retrieve relevant chunks using keyword search."

With a vector database, Step 2 becomes:
1. Convert the user's question to a vector using the embedding model
2. Search the vector database for the most similar document vectors
3. Return the original text of those documents

Steps 1 and 3 are identical. Only the retrieval method changes. But that change makes the whole system work for natural, varied language instead of only exact keyword matches.

---

## Now go do the practical

Open `try-it-yourself.md`. You will build a semantic search system using Chroma and a free embedding model, then compare it directly against the keyword search from Chapter 6.

---

## Going deeper (optional)

Open `deep-dive.md` to understand how embedding models are trained, what dimensionality means, and how to choose between vector database options.

---

## Check yourself

Open `test.md` before moving to Chapter 8.
