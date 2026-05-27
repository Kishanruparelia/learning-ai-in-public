# Try it yourself: Chapter 7

Three practicals. 30 minutes total. Do them in order.

---

## Practical 1: See what an embedding looks like (5 min)

Open colab.research.google.com and create a new notebook. Paste and run this:

```python
# Install the libraries we need
# sentence-transformers: free, open-source embedding model that runs locally
# chromadb: vector database that runs in memory, no setup needed
!pip install sentence-transformers chromadb groq -q

from sentence_transformers import SentenceTransformer

# Load a small, fast embedding model
# This runs entirely on your machine, no API key needed
model = SentenceTransformer("all-MiniLM-L6-v2")

# Convert 3 sentences to vectors
sentences = [
    "How do I reset my password?",
    "Steps to change my login credentials",
    "Best pizza restaurants in the city"
]

embeddings = model.encode(sentences)

# Show what an embedding looks like
print(f"Each embedding has {len(embeddings[0])} numbers")
print(f"\nFirst 10 numbers of sentence 1: {embeddings[0][:10].round(3)}")
print(f"First 10 numbers of sentence 2: {embeddings[1][:10].round(3)}")
print(f"First 10 numbers of sentence 3: {embeddings[2][:10].round(3)}")
```

Run it. You will see that sentences 1 and 2 (which mean similar things) have similar-looking numbers, while sentence 3 (unrelated topic) looks very different.

---

## Practical 2: Build semantic search with a vector database (15 min)

Add a new cell. This replaces the keyword search from Chapter 6 with proper semantic search:

```python
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from google.colab import userdata

# Load embedding model and LLM client
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
llm = Groq(api_key=userdata.get("GROQ_API_KEY"))

# ---- STEP 1: INDEX DOCUMENTS INTO VECTOR DATABASE ----

# Same policy documents as Chapter 6
documents = [
    {"id": "1", "topic": "parental leave",  "content": "All full-time employees are entitled to 26 weeks of paid parental leave upon the birth or adoption of a child. This applies equally to all parents. Leave can be taken in one block or split into two periods within the first year."},
    {"id": "2", "topic": "sick leave",      "content": "Employees receive 12 days of paid sick leave per calendar year. Unused sick leave does not carry over to the next year. A medical certificate is required for absences longer than 3 consecutive days."},
    {"id": "3", "topic": "annual leave",    "content": "Employees receive 20 days of paid annual leave per year after completing 6 months of service. Leave requests must be submitted at least 2 weeks in advance. Up to 5 unused days can be carried over to the following year."},
    {"id": "4", "topic": "work from home",  "content": "Employees may work from home up to 3 days per week with manager approval. Home office equipment allowance is available for eligible employees. Core hours of 10am to 4pm must be maintained regardless of work location."},
    {"id": "5", "topic": "reimbursement",   "content": "Business travel expenses must be submitted within 30 days of travel using the reimbursement portal. Meals are reimbursed up to a daily limit for domestic travel. Flight bookings above a certain amount require prior manager approval."}
]

# Set up an in-memory Chroma vector database
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("company_policies")

# Embed each document and store in Chroma
for doc in documents:
    embedding = embed_model.encode(doc["content"]).tolist()
    collection.add(
        ids=[doc["id"]],
        embeddings=[embedding],
        documents=[doc["content"]],
        metadatas=[{"topic": doc["topic"]}]
    )

print(f"Indexed {len(documents)} documents into the vector database.")

# ---- STEP 2: SEMANTIC RETRIEVAL ----

def retrieve_semantic(question, top_n=2):
    # Convert question to vector
    query_embedding = embed_model.encode(question).tolist()

    # Search for most similar documents
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_n
    )

    retrieved = []
    for i in range(len(results["documents"][0])):
        retrieved.append({
            "content": results["documents"][0][i],
            "topic": results["metadatas"][0][i]["topic"],
            "similarity": round(1 - results["distances"][0][i], 3)
        })
    return retrieved

# ---- STEP 3: AUGMENT AND GENERATE ----

def ask_with_semantic_rag(question):
    docs = retrieve_semantic(question)
    context = "\n\n".join([f"Policy: {d['topic'].title()}\n{d['content']}" for d in docs])

    prompt = f"""CONTEXT (use only this to answer):
{context}

QUESTION: {question}

Answer based only on the context. If the answer is not there, say "I don't have that information." """

    response = llm.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    print(f"\nQ: {question}")
    print(f"A: {response.choices[0].message.content}")
    print(f"[Retrieved: {[(d['topic'], d['similarity']) for d in docs]}]")
```

Run it to set everything up. Then add another cell and test it:

```python
# These are the questions that BROKE keyword search in Chapter 6
# Now watch semantic search handle them correctly

ask_with_semantic_rag("How many vacation days do I get per year?")
# "vacation days" is not in the document but "annual leave" is

ask_with_semantic_rag("Where do I submit my expense claim?")
# "expense claim" vs "reimbursement portal" in the document

ask_with_semantic_rag("I just had a baby. What leave am I entitled to?")
# Very different wording from the document but same meaning

ask_with_semantic_rag("Do I need a doctor's note if I am ill for a week?")
# Paraphrasing the sick leave policy using completely different words
```

Run it. All four of these failed with keyword search in Chapter 6. With semantic search, all four should retrieve the right document and answer correctly.

---

## Practical 3: Compare keyword vs semantic side by side (10 min)

Add a new cell to see the two approaches fail and succeed on the same question:

```python
# Keyword search from Chapter 6 (copied here for comparison)
def retrieve_keyword(question, documents, top_n=2):
    question_words = question.lower().split()
    scored = []
    for doc in documents:
        doc_text = (doc["topic"] + " " + doc["content"]).lower()
        score = sum(1 for word in question_words if word in doc_text)
        scored.append((score, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = [doc for score, doc in scored[:top_n] if score > 0]
    return top

# Test the same question both ways
test_question = "How many vacation days do I get?"

keyword_results = retrieve_keyword(test_question, documents)
semantic_results = retrieve_semantic(test_question)

print("KEYWORD SEARCH retrieved:")
print([d["topic"] for d in keyword_results] if keyword_results else "Nothing found")

print("\nSEMANTIC SEARCH retrieved:")
print([(d["topic"], d["similarity"]) for d in semantic_results])
```

Run it. Keyword search will return nothing or the wrong document. Semantic search will correctly return the annual leave policy even though the words do not match.

---

## What to show me before moving to Chapter 8

1. A screenshot showing semantic search correctly answering the "vacation days" question that keyword search failed on
2. A one-line answer to: "What is the key difference between how keyword search and semantic search find documents?"
