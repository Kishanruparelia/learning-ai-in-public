# Deep dive: How embedding models and vector databases work

Optional reading. Skip if you just want to use AI. Read if you want to understand it.

---

## How embedding models are trained

An embedding model is trained to place similar-meaning text close together in vector space.

One common training method is called contrastive learning:

1. Take pairs of sentences that mean the same thing (e.g., from translation pairs, or question-answer pairs).
2. Train the model to produce vectors that are close together for similar pairs and far apart for unrelated pairs.
3. After training on millions of such pairs, the model generalises to any new sentence.

The model you used in the practical, `all-MiniLM-L6-v2`, was trained on over 1 billion sentence pairs. It produces 384-dimensional vectors, meaning each sentence becomes a list of 384 numbers.

---

## What dimensionality means

A 384-dimensional vector means the meaning of a sentence is represented across 384 different axes.

You can think of each dimension as capturing a different aspect of meaning. Some dimensions might loosely correspond to concepts like formality, topic domain, sentiment, or specificity. But unlike manually designed features, these dimensions are learned automatically and are not human-interpretable.

Larger models produce higher-dimensional vectors (OpenAI's text-embedding-3-large produces 3072 dimensions). Higher dimensions generally mean better accuracy at finding similar meaning, but also more storage and slower search.

For most applications, 384 to 1536 dimensions is plenty.

---

## Cosine similarity vs dot product vs Euclidean distance

There are three common ways to measure how similar two vectors are:

**Cosine similarity:** Measures the angle between two vectors. Ranges from -1 to 1. Most commonly used for text embeddings because it is not affected by vector magnitude, only direction.

**Dot product:** Multiplies corresponding numbers and sums them. Fast to compute. Used in some production systems.

**Euclidean distance:** Straight-line distance between two points. Less common for text because magnitude matters and embeddings are usually normalised.

Chroma uses cosine distance by default (1 minus cosine similarity, so lower is more similar).

---

## Approximate nearest neighbour search

If you have 1 million vectors and a user asks a question, you cannot compare the query to all 1 million exactly. That would take too long.

Vector databases use algorithms like HNSW (Hierarchical Navigable Small World) or IVF (Inverted File Index) to find the closest vectors approximately but very quickly.

"Approximately" means it might miss 1 or 2 of the true top matches in rare cases. In practice, for text similarity tasks, the error rate is negligible and the speed gain is enormous: milliseconds instead of seconds.

---

## Choosing a vector database

| Option | Best for |
|--------|----------|
| Chroma | Learning, prototypes, runs in memory or locally |
| Pinecone | Managed cloud service, easy to scale, pay as you go |
| Weaviate | Open source, rich filtering alongside vectors, self-hosted or cloud |
| Qdrant | Open source, fast, good for high-performance production |
| pgvector | You already use PostgreSQL and want to add vector search without a new database |
| Milvus | Very large scale, billions of vectors |

For a prototype or small internal tool, Chroma running locally is perfectly fine. For a production system with many users or a large document base, a managed service like Pinecone or a self-hosted Qdrant is more appropriate.

---

## Metadata filtering

Vector databases support filtering by metadata alongside the vector search.

Example: You have a knowledge base of support articles. Each article has metadata like `category`, `language`, and `last_updated`.

A user query can combine vector similarity with a metadata filter:
- "Find the articles most similar to this question, but only from the 'billing' category and only updated in the last 6 months."

This dramatically improves retrieval precision for large, diverse knowledge bases. Pure similarity search over everything often returns technically similar but contextually wrong results. Metadata filtering keeps the search in the right neighbourhood first.

---

## The embedding model must stay consistent

If you embed your documents with Model A and later switch to Model B, all your stored vectors become useless. Model B operates in a completely different vector space. Similarity scores between Model A documents and Model B queries will be meaningless.

This means: once you choose an embedding model for a production system, changing it requires re-embedding your entire document collection. Plan your model choice carefully upfront.
