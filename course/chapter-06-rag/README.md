# Chapter 6: RAG (Retrieval Augmented Generation)

**Time needed:** 1 hour
**You will need:** A browser, your Groq API key, Google Colab open

---

## What you will be able to do by the end

1. Explain what RAG is and the problem it solves
2. Understand the 3 steps every RAG system follows
3. Build a simple RAG pipeline in Colab using plain text documents
4. Know when RAG is the right solution and when it is not

---

## The big idea

An LLM knows a lot, but it does not know your stuff.

It does not know your company's latest HR policy. It does not know what changed in your product last week. It does not know the contents of a document a user just uploaded.

RAG is the fix. Instead of relying on what the model memorised during training, you retrieve the relevant information at the moment of the question and hand it directly to the model. The model reads it and answers from that.

It is the difference between asking someone to answer from memory and handing them the relevant page to read first.

---

## The problem RAG solves

Without RAG, an LLM has two big limitations:

**1. Knowledge cutoff**
The model was trained on data up to a certain date. Anything after that date, it does not know. Ask it about something that changed last month and it will either say it does not know or, worse, hallucinate an outdated answer.

**2. Private knowledge**
The model was trained on public internet data. Your internal documents, your product manuals, your company policies, your customer records: none of that is in the model.

RAG solves both by treating the model as a reader and reasoner, not a memory bank.

---

## How RAG works: 3 steps

### Step 1: Index your documents

Before any user asks a question, you take your documents and store them in a way that makes them searchable.

For simple RAG, this means loading your text documents into a list or a database.

For production RAG, this means converting each document (or chunk of a document) into a vector, a mathematical representation of its meaning, and storing those vectors in a vector database. We cover vectors in Chapter 7.

### Step 2: Retrieve the relevant chunks

When a user asks a question, your system searches the document store for the pieces most relevant to that question.

Simple version: keyword search. Find documents that contain the words in the question.

Production version: semantic search. Find documents that mean the same thing as the question, even if the words are different.

### Step 3: Augment the prompt and generate

Take the retrieved chunks and paste them into the prompt, right before the user's question. Tell the model to answer only from what you just gave it.

```
CONTEXT:
[retrieved document chunks go here]

USER QUESTION:
[the user's actual question]

Answer using only the information in the CONTEXT above.
If the answer is not in the context, say "I don't have that information."
```

The model reads the context, finds the answer, and replies. It is not guessing from memory. It is reading.

---

## A real example

**Scenario:** A company has a 50-page employee handbook. They want an AI assistant that answers employee questions about leave policy, reimbursements, and benefits.

**Without RAG:**
Employee asks: "How many sick days am I entitled to per year?"
The model guesses based on general knowledge. Gets it wrong for this specific company's policy.

**With RAG:**
1. The handbook is indexed into chunks.
2. The question "sick days per year" retrieves the relevant section from the handbook.
3. That section is pasted into the prompt.
4. The model reads the actual policy and answers correctly.

The model did not need to know the policy. It just needed to read it.

---

## What RAG is good at

| Use case | Why RAG works |
|----------|---------------|
| Q&A over internal documents | Documents are private, not in training data |
| Customer support using a product manual | Manual changes often, can't retrain the model |
| Policy or compliance queries | Exact wording matters, memory cannot be trusted |
| Searching a large knowledge base | Too much content to fit in one prompt |
| Answering questions about recent events | After the model's knowledge cutoff |

---

## What RAG is not good at

| Use case | Why RAG struggles |
|----------|------------------|
| Open-ended creative tasks | No document to retrieve from |
| Questions that need reasoning across many documents | Retrieved chunks may miss the connection |
| Real-time data (live stock prices, live inventory) | RAG retrieves stored documents, not live feeds |
| When the user's question is very vague | Hard to retrieve the right chunk without a clear query |

---

## The simple version vs the full version

In this chapter you will build the simplest possible RAG: a Python list of documents, keyword matching to find relevant ones, and Groq to answer the question.

This is not production RAG. But it teaches the exact same 3-step logic. Once you understand the logic, swapping in a real vector database and semantic search is just upgrading the retrieval step.

---

## Now go do the practical

Open `try-it-yourself.md`. You will build a working RAG pipeline in about 30 lines of code.

---

## Going deeper (optional)

Open `deep-dive.md` to understand what vector embeddings are, how semantic search works, and what a production RAG stack looks like.

---

## Check yourself

Open `test.md` before moving to Chapter 7.
