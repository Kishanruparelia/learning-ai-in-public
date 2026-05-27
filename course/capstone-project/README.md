# Capstone Project: Build an AI Support Assistant

**Estimated time:** 2 to 3 hours
**Chapters used:** All 10
**You will need:** Google Colab, your Groq API key

---

## What you are building

A working AI-powered customer support assistant that can:

1. Answer questions from a knowledge base (not from memory)
2. Classify the type of request automatically
3. Stay within guardrails using a system prompt
4. Use a tool to look up live order status
5. Evaluate its own response quality
6. Report its token cost per conversation

This is not a toy. Every component maps directly to what real AI products do in production.

---

## The scenario

You are building the AI support assistant for a fictional online electronics store called **ByteShop**.

ByteShop has:
- A knowledge base of product and policy information
- An order status lookup system
- A customer support team that needs AI assistance

Your assistant, named **Nova**, will handle incoming customer queries.

---

## The knowledge base

Nova will answer from this knowledge base only. She does not guess.

```
BYTESHOP KNOWLEDGE BASE

1. RETURN POLICY
ByteShop accepts returns within 30 days of delivery for all products.
Items must be unused and in original packaging. Electronics with opened
packaging can only be returned if faulty. Refunds are processed within
5 to 7 business days after the returned item is received.

2. WARRANTY
All electronics carry a 12-month manufacturer warranty.
Accessories (cables, cases, stands) carry a 6-month warranty.
Warranty claims must be submitted through the ByteShop warranty portal.
Physical damage and water damage are not covered under warranty.

3. SHIPPING
Standard delivery: 3 to 5 business days. Free on orders above Rs 999.
Express delivery: 1 to 2 business days. Flat fee of Rs 149.
Same-day delivery is available in Mumbai, Delhi, and Bangalore only.
International shipping is not available.

4. PAYMENT
ByteShop accepts UPI, credit cards, debit cards, and net banking.
EMI is available on orders above Rs 5,000 with eligible cards.
Cash on delivery is available for orders below Rs 10,000.

5. ACCOUNT AND ORDERS
Orders can be cancelled within 2 hours of placement.
After 2 hours, cancellation is not possible but returns apply after delivery.
To track an order, use the Track Order section on the website or app.
For account issues, contact support@byteshop.in.
```

---

## Build instructions

Open Google Colab and build Nova step by step. Each step maps to a chapter.

---

### Step 1: Set up and load the knowledge base (Chapter 6)

```python
!pip install groq sentence-transformers chromadb -q

from groq import Groq
from google.colab import userdata
from sentence_transformers import SentenceTransformer
import chromadb
import json
import time

llm = Groq(api_key=userdata.get("GROQ_API_KEY"))
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Knowledge base chunks
kb = [
    {"id": "1", "topic": "return policy",   "content": "ByteShop accepts returns within 30 days of delivery for all products. Items must be unused and in original packaging. Electronics with opened packaging can only be returned if faulty. Refunds are processed within 5 to 7 business days after the returned item is received."},
    {"id": "2", "topic": "warranty",        "content": "All electronics carry a 12-month manufacturer warranty. Accessories carry a 6-month warranty. Warranty claims must be submitted through the ByteShop warranty portal. Physical damage and water damage are not covered."},
    {"id": "3", "topic": "shipping",        "content": "Standard delivery: 3 to 5 business days. Free on orders above Rs 999. Express delivery: 1 to 2 business days at Rs 149. Same-day delivery in Mumbai, Delhi, and Bangalore only. No international shipping."},
    {"id": "4", "topic": "payment",         "content": "ByteShop accepts UPI, credit cards, debit cards, and net banking. EMI available on orders above Rs 5,000. Cash on delivery available for orders below Rs 10,000."},
    {"id": "5", "topic": "orders accounts", "content": "Orders can be cancelled within 2 hours of placement. After 2 hours, cancellation is not possible but returns apply after delivery. Track orders on the website or app. For account issues contact support@byteshop.in."},
]

# Index into vector database (Chapter 7)
chroma = chromadb.Client()
collection = chroma.create_collection("byteshop_kb")

for doc in kb:
    embedding = embed_model.encode(doc["content"]).tolist()
    collection.add(ids=[doc["id"]], embeddings=[embedding],
                   documents=[doc["content"]], metadatas=[{"topic": doc["topic"]}])

def retrieve(question, top_n=2):
    query_vec = embed_model.encode(question).tolist()
    results = collection.query(query_embeddings=[query_vec], n_results=top_n)
    return results["documents"][0]

print("Knowledge base indexed.")
```

---

### Step 2: Build the system prompt (Chapter 5)

```python
NOVA_SYSTEM_PROMPT = """You are Nova, the AI customer support assistant for ByteShop, an online electronics store.

PERSONA: Friendly, clear, and efficient. You care about solving the customer's problem.

SCOPE: You only answer questions about ByteShop products, policies, shipping, payments, returns, and orders.
If asked about anything unrelated, politely say you can only help with ByteShop topics.

RULES:
- Answer ONLY from the context provided. Do not add information from your general knowledge.
- If the answer is not in the context, say: "I don't have that information. Please contact support@byteshop.in."
- Never make up order details, prices, or timelines that are not in the context.
- Keep replies under 4 sentences unless the customer needs step-by-step instructions.

OUTPUT: End every reply with one follow-up question to confirm the customer's need was met."""
```

---

### Step 3: Add a tool for order lookup (Chapter 9)

```python
# Simulated order database
orders_db = {
    "ORD-1001": {"status": "delivered",    "item": "Wireless Keyboard",  "date": "2 days ago"},
    "ORD-1002": {"status": "in transit",   "item": "Laptop Stand",       "date": "expected tomorrow"},
    "ORD-1003": {"status": "processing",   "item": "USB-C Hub",          "date": "ships within 24 hours"},
    "ORD-1004": {"status": "cancelled",    "item": "Monitor",            "date": "refund in 5 to 7 days"},
}

tools = [{
    "type": "function",
    "function": {
        "name": "lookup_order",
        "description": "Looks up the status of a customer order using the order ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "The order ID, e.g. ORD-1001"}
            },
            "required": ["order_id"]
        }
    }
}]

def lookup_order(order_id):
    order = orders_db.get(order_id.upper())
    if order:
        return order
    return {"error": f"Order {order_id} not found. Please check the order ID."}
```

---

### Step 4: Build the full assistant (Chapters 3, 4, 5, 6, 7, 9, 10)

```python
def nova(customer_message):
    print(f"\n CUSTOMER: {customer_message}")

    # Retrieve relevant knowledge (Chapters 6 + 7)
    context_chunks = retrieve(customer_message)
    context = "\n\n".join(context_chunks)

    # Build the augmented user message (Chapter 4 - grounding)
    augmented = f"""CONTEXT FROM BYTESHOP KNOWLEDGE BASE:
{context}

CUSTOMER MESSAGE:
{customer_message}"""

    messages = [
        {"role": "system", "content": NOVA_SYSTEM_PROMPT},
        {"role": "user",   "content": augmented}
    ]

    # Track tokens for cost reporting (Chapter 10)
    start = time.time()

    # First call - may include a tool call (Chapter 9)
    response = llm.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0
    )

    message = response.choices[0].message
    total_input = response.usage.prompt_tokens
    total_output = response.usage.completion_tokens

    # Handle tool call if model requested one
    if message.tool_calls:
        messages.append(message)
        for tc in message.tool_calls:
            args = json.loads(tc.function.arguments)
            print(f" [TOOL] lookup_order({args})")
            result = lookup_order(**args)
            print(f" [RESULT] {result}")
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(result)})

        # Second call with tool result
        response = llm.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0
        )
        total_input  += response.usage.prompt_tokens
        total_output += response.usage.completion_tokens

    elapsed = time.time() - start
    reply = response.choices[0].message.content

    print(f"\n NOVA: {reply}")

    # Cost report (Chapter 10)
    cost = (total_input * 0.59 + total_output * 0.79) / 1_000_000
    print(f"\n [Tokens: {total_input} in / {total_output} out | Cost: ${cost:.6f} | Time: {elapsed:.2f}s]")

    return reply
```

---

### Step 5: Add an evaluator (Chapter 8)

```python
def evaluate_reply(customer_message, nova_reply):
    judge_prompt = f"""You are evaluating a customer support reply.

CUSTOMER MESSAGE: {customer_message}
SUPPORT REPLY: {nova_reply}

Score from 1 to 5 on:
- accuracy: does it answer correctly without making things up?
- helpfulness: does it actually solve the customer's need?
- tone: is it friendly and professional?

Return ONLY valid JSON: {{"accuracy": 0, "helpfulness": 0, "tone": 0}}"""

    r = llm.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": judge_prompt}],
        temperature=0
    )
    raw = r.choices[0].message.content
    scores = json.loads(raw[raw.find("{"):raw.rfind("}")+1])
    total = sum(scores.values())
    print(f" [EVAL] Accuracy: {scores['accuracy']}/5 | Helpfulness: {scores['helpfulness']}/5 | Tone: {scores['tone']}/5 | Total: {total}/15")
    return scores
```

---

### Step 6: Run Nova end to end

```python
# Test with 6 different customer queries
test_queries = [
    "Can I return my laptop if I already opened the box?",
    "How long does standard shipping take and is it free?",
    "What is the status of my order ORD-1002?",
    "Do you ship to London?",
    "My keyboard stopped working after 8 months. Is it under warranty?",
    "Can I pay in EMI for a Rs 3,000 purchase?",
]

print("=" * 60)
print("NOVA - ByteShop AI Support Assistant")
print("=" * 60)

scores_all = []
for query in test_queries:
    reply = nova(query)
    scores = evaluate_reply(query, reply)
    scores_all.append(scores)
    print()

# Summary report
avg_accuracy    = sum(s["accuracy"]    for s in scores_all) / len(scores_all)
avg_helpfulness = sum(s["helpfulness"] for s in scores_all) / len(scores_all)
avg_tone        = sum(s["tone"]        for s in scores_all) / len(scores_all)

print("=" * 60)
print("NOVA PERFORMANCE SUMMARY")
print(f"Accuracy:    {avg_accuracy:.1f}/5")
print(f"Helpfulness: {avg_helpfulness:.1f}/5")
print(f"Tone:        {avg_tone:.1f}/5")
print(f"Overall:     {(avg_accuracy + avg_helpfulness + avg_tone):.1f}/15")
print("=" * 60)
```

---

## What good output looks like

- Nova answers return/warranty/shipping questions accurately from the knowledge base
- Nova calls the order lookup tool when given an order ID
- Nova refuses to answer off-topic questions
- Nova correctly says it does not know when the knowledge base has no answer
- The evaluator scores 4/5 or above on most queries

---

## What to submit

1. A screenshot of Nova answering at least 4 of the 6 test queries
2. A screenshot of the performance summary at the end
3. One sentence: what would you add to Nova if this were a real product?

---

## Chapters used in this capstone

| Step | Chapter |
|------|---------|
| Knowledge base indexing | Chapter 6: RAG |
| Semantic retrieval | Chapter 7: Vector Databases |
| System prompt and guardrails | Chapter 5: System Prompts |
| Hallucination prevention | Chapter 4: Hallucinations |
| Prompting and output format | Chapter 3: Prompting |
| Tool use for order lookup | Chapter 9: Agents and Tool Use |
| Token cost reporting | Chapter 10: Cost, Latency, Model Selection |
| LLM-as-a-judge evaluation | Chapter 8: Evaluations |
| Understanding token limits | Chapter 2: Tokens |
| Understanding why the model behaves as it does | Chapter 1: What is an LLM |
