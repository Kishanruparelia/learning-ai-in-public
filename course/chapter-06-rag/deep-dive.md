# Deep dive: How production RAG actually works

Optional reading. Skip if you just want to use AI. Read if you want to understand it.

---

## The problem with keyword search

The simple RAG you built in the practical used keyword matching. If the question contains a word that appears in the document, it gets retrieved.

This breaks in two common ways:

**Vocabulary mismatch:** The user says "vacation days", the document says "annual leave". Same meaning, different words. Keyword search misses it.

**Too many matches:** The user asks a specific question, but many documents contain the keywords. You retrieve the wrong ones.

The fix is semantic search, which understands meaning rather than just matching words.

---

## What are vector embeddings

An embedding is a way of converting text into a list of numbers that represents its meaning.

Example (simplified):
- "I want to take time off work" might become [0.82, 0.14, 0.67, ...]
- "annual leave policy" might become [0.79, 0.18, 0.71, ...]
- "stock market trading" might become [0.12, 0.91, 0.04, ...]

The first two are close in meaning, so their numbers are similar. The third is about a different topic entirely, so its numbers are very different.

When you search semantically, you convert the user's question into an embedding, then find the documents whose embeddings are closest to it. This works even when the words are completely different, as long as the meaning is similar.

---

## Vector databases

A vector database is built specifically to store embeddings and run fast similarity searches over millions of them.

Common vector databases: Pinecone, Weaviate, Chroma, Qdrant, pgvector (a PostgreSQL extension).

The production RAG flow:

1. **At index time:** For each document chunk, call an embedding model to get its vector. Store the vector and the original text in the vector database.

2. **At query time:** Convert the user's question into a vector using the same embedding model. Search the vector database for the most similar vectors. Return the original text of those documents.

3. **Generate:** Paste the retrieved text into the prompt. Ask the LLM to answer from it.

The LLM never sees the vector. It only sees the retrieved text. Vectors are only used for finding the right documents quickly.

---

## Chunking strategy

One of the most important decisions in RAG is how to split your documents into chunks.

**Too large:** The chunk contains too much information. The relevant sentence is buried in a wall of text. The model may miss it or get distracted.

**Too small:** The chunk loses context. A sentence about "26 weeks of leave" without the surrounding paragraph might not make clear what type of leave it refers to.

Common strategies:
- Fixed size (e.g., 500 tokens per chunk) with overlap (last 50 tokens of chunk N are the first 50 of chunk N+1)
- Split by paragraph or section heading
- Split by semantic meaning (more complex, uses an LLM to identify topic boundaries)

There is no single right answer. The best chunking strategy depends on your document structure.

---

## Retrieval quality matters more than generation quality

A common mistake: spending weeks fine-tuning prompts and ignoring the retrieval step.

If the retrieval returns the wrong documents, no amount of prompt engineering will fix the answer. The model is reading the wrong page.

The retrieval step is the foundation. If you have a RAG system that is giving wrong answers, the first thing to check is: are the right documents being retrieved? Log what gets retrieved for each query and look at it manually.

---

## Hybrid search

Production RAG systems often combine keyword search and semantic search.

Keyword search is very good at exact matches: product codes, names, specific dates.
Semantic search is good at meaning-based matches: synonyms, paraphrases, concepts.

Hybrid search runs both and combines the results. This gives better coverage than either alone.

---

## What a production RAG stack looks like

1. **Document ingestion pipeline:** Reads PDFs, Word docs, web pages, databases. Cleans the text. Splits into chunks. Generates embeddings. Stores in vector database.

2. **Query pipeline:** Takes user question. Generates its embedding. Searches vector database. Retrieves top N chunks. Builds the augmented prompt. Calls the LLM. Returns the answer.

3. **Evaluation loop:** Periodically checks whether the system is retrieving the right documents and generating correct answers. Adjusts chunking, retrieval parameters, or prompts based on failures.

Building the first version takes a few days. Making it reliable for production takes weeks of evaluation and tuning.
