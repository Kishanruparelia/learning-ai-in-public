# Try it yourself: Chapter 6

Three practicals. 30 minutes total. Do them in order.

---

## Practical 1: See the problem RAG solves (5 min)

Open colab.research.google.com and create a new notebook. Paste and run this:

```python
!pip install groq -q
from groq import Groq
from google.colab import userdata

client = Groq(api_key=userdata.get("GROQ_API_KEY"))

def ask(prompt, system="", label=""):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=messages
    )
    print(f"\n--- {label} ---")
    print(response.choices[0].message.content)

# Ask the model a question about a fictional company policy
# The model has never seen this policy, so it will guess or refuse

ask(
    "According to our leave policy, how many days of paid parental leave does a new parent get?",
    label="NO RAG - model guessing from memory"
)
```

Run it. The model will either say it does not know, or it will guess a number based on general knowledge. Either way, it is not answering from your actual policy.

---

## Practical 2: Build a simple RAG pipeline (20 min)

Add a new cell. This is the full simple RAG implementation:

```python
# ---- STEP 1: INDEX YOUR DOCUMENTS ----
# In real RAG, these would be chunks from a PDF or database.
# Here we use a simple Python list as our "knowledge base".

documents = [
    {
        "id": 1,
        "topic": "parental leave",
        "content": "All full-time employees are entitled to 26 weeks of paid parental leave upon the birth or adoption of a child. This applies equally to all parents. Leave can be taken in one block or split into two periods within the first year."
    },
    {
        "id": 2,
        "topic": "sick leave",
        "content": "Employees receive 12 days of paid sick leave per calendar year. Unused sick leave does not carry over to the next year. A medical certificate is required for absences longer than 3 consecutive days."
    },
    {
        "id": 3,
        "topic": "annual leave",
        "content": "Employees receive 20 days of paid annual leave per year after completing 6 months of service. Leave requests must be submitted at least 2 weeks in advance. Up to 5 unused days can be carried over to the following year."
    },
    {
        "id": 4,
        "topic": "work from home",
        "content": "Employees may work from home up to 3 days per week with manager approval. Home office equipment allowance is Rs 15,000 per year for eligible employees. Core hours of 10am to 4pm must be maintained regardless of work location."
    },
    {
        "id": 5,
        "topic": "reimbursement",
        "content": "Business travel expenses must be submitted within 30 days of travel using the reimbursement portal. Meals are reimbursed up to Rs 500 per day for domestic travel. Flight bookings above Rs 8,000 require prior manager approval."
    }
]

# ---- STEP 2: RETRIEVE RELEVANT DOCUMENTS ----
# Simple retrieval: check if any keyword from the question
# appears in the document's topic or content.
# Production RAG uses semantic (meaning-based) search instead.

def retrieve(question, documents, top_n=2):
    question_words = question.lower().split()
    scored = []

    for doc in documents:
        # Count how many question words appear in this document
        doc_text = (doc["topic"] + " " + doc["content"]).lower()
        score = sum(1 for word in question_words if word in doc_text)
        scored.append((score, doc))

    # Sort by score, return top matches
    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for score, doc in scored[:top_n] if score > 0]

# ---- STEP 3: AUGMENT THE PROMPT AND GENERATE ----
def ask_with_rag(question):
    # Retrieve relevant chunks
    relevant_docs = retrieve(question, documents)

    if not relevant_docs:
        print("\nNo relevant documents found. Cannot answer this question.")
        return

    # Build context string from retrieved documents
    context = "\n\n".join([f"Policy: {doc['topic'].title()}\n{doc['content']}" for doc in relevant_docs])

    # Build the augmented prompt
    augmented_prompt = f"""CONTEXT (use only this information to answer):
{context}

QUESTION: {question}

Answer based only on the context above. If the answer is not in the context, say "I don't have that information in our policy documents." """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[{"role": "user", "content": augmented_prompt}]
    )

    print(f"\nQ: {question}")
    print(f"A: {response.choices[0].message.content}")
    print(f"\n[Retrieved from: {[doc['topic'] for doc in relevant_docs]}]")

# Test with several questions
ask_with_rag("How many days of parental leave do I get?")
ask_with_rag("Can I work from home every day?")
ask_with_rag("What is the deadline to submit travel reimbursements?")
ask_with_rag("How many sick days can I carry over to next year?")
ask_with_rag("What is the salary increment policy?")  # Not in our documents
```

Run it. For every question, you will see:
- The answer the model gave
- Which documents were retrieved to answer it

Notice the last question. "Salary increment policy" is not in our document list. The model should say so rather than hallucinating an answer.

**What to notice:** The model is not guessing. It is reading. Its accuracy now depends on the quality of your documents, not its training data.

---

## Practical 3: Break the retrieval and see what happens (5 min)

Add a new cell. We will test what happens when retrieval finds the wrong document:

```python
# Ask a question using different words than what is in the documents
# Our document says "annual leave" but the user says "vacation days"

ask_with_rag("How many vacation days do I get per year?")

# Our document says "reimbursement portal" but user says "expense claim"
ask_with_rag("Where do I submit my expense claim?")
```

Run it. The simple keyword retrieval may fail to find the right document because the words do not match exactly.

This is the core limitation of simple keyword RAG. The user says "vacation days", the document says "annual leave", and the retrieval misses it.

This is exactly why production RAG uses semantic (meaning-based) search instead. Semantic search understands that "vacation days" and "annual leave" mean the same thing. We cover that in Chapter 7.

---

## What to show me before moving to Chapter 7

1. A screenshot showing the RAG pipeline answering the parental leave question correctly
2. A one-line answer to: "What happened when you asked about vacation days, and why?"
