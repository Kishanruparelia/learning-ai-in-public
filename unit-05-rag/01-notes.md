# Unit 5: RAG (Retrieval Augmented Generation)

## Stage 1: Concept

---

### The problem RAG solves

The model is frozen in time (Unit 1). Factual hallucinations happen because it predicts a plausible answer instead of fetching the real one (Unit 4). RAG is the fix.

---

### The open book exam analogy

**Closed book:** walk in with only what is in your head. If you forgot something, you guess. Sometimes confidently wrong.

**Open book:** walk in with notes and references. Before answering, look up the relevant page. Answer is grounded in actual material, not memory.

A standard LLM is always closed book. RAG makes it open book.

---

### What RAG stands for

**Retrieval:** go find the relevant information from a knowledge base.
**Augmented:** add that information into the prompt.
**Generation:** let the model answer using what it just found, not its training memory.

---

### The 5 steps of RAG

Example: user asks "What is our refund policy for premium subscribers?"

1. User question comes in.
2. System searches the knowledge base (policy docs, product docs, database) for relevant content.
3. Relevant chunks are retrieved. Example: 3 paragraphs from the refund policy document.
4. Those chunks are injected into the prompt alongside the question. Model sees: "Here is the relevant policy: [retrieved text]. Answer using only this."
5. Model generates a response grounded in the actual document. Serve with citations so the user can verify.

**Always cite sources in RAG products.** Citations build trust and catch cases where retrieval pulled the wrong document.

---

### The library analogy

A massive library. User walks in and asks a question. The librarian does not read every book. They check the index, find the 3 most relevant pages, and hand just those to the reader.

That index is called a vector database. Unit 6 covers it. For now just know it makes retrieval fast and accurate at scale.

---

### What RAG fixes and what it does not

RAG fixes: Factual hallucinations where the model lacks current or specific information.

RAG does not fix: Logical hallucinations (need chain of thought), Instruction hallucinations (need system prompts), Fabrication where the model invents things even when given documents.

RAG is not magic. If your knowledge base has wrong or outdated documents, the model answers confidently using that wrong content. Garbage in, garbage out applies to your knowledge base too.

---

### Why every serious AI product uses RAG

A customer support bot needs your actual FAQs, not generic training data.
A research assistant needs your actual reports, not approximations.
A legal tool needs the actual contracts and regulations, not what the model vaguely remembers.

The model alone is too general. RAG is what makes it specific to your business.

---

### Self check

1. What does RAG stand for? What does each word mean?
2. What is the open book vs closed book difference?
3. Walk through the 5 steps for an HR policy question.

**Answers:**
1. Retrieval Augmented Generation. Retrieve relevant data, augment the prompt with it, generate response from that data.
2. Without RAG: closed book, model answers from frozen memory, guesses when it does not know. With RAG: open book, model fetches relevant content first, answers from actual documents.
3. User prompt comes in. RAG retrieves relevant policy paragraphs. Data plus prompt injected into LLM. LLM generates response. Served to user with citations.
