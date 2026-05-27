# Try it yourself: Chapter 10

Three practicals. 30 minutes total. Do them in order.

---

## Practical 1: Measure real token usage and latency (10 min)

Open colab.research.google.com and create a new notebook. Paste and run this:

```python
!pip install groq -q
from groq import Groq
from google.colab import userdata
import time

client = Groq(api_key=userdata.get("GROQ_API_KEY"))

def call_and_measure(system, user, model="llama-3.3-70b-versatile", label=""):
    start = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    )
    elapsed = time.time() - start

    usage = response.usage
    print(f"\n--- {label} ---")
    print(f"Input tokens:  {usage.prompt_tokens}")
    print(f"Output tokens: {usage.completion_tokens}")
    print(f"Total tokens:  {usage.total_tokens}")
    print(f"Latency:       {elapsed:.2f}s")
    print(f"Reply preview: {response.choices[0].message.content[:120]}...")
    return usage.prompt_tokens, usage.completion_tokens, elapsed

# Same task, two system prompt lengths
short_system = "You are a helpful customer support assistant. Be concise."

long_system = """You are a highly professional and knowledgeable customer support assistant
working for a technology company. Your role is to assist customers with their queries
in a helpful, empathetic, and professional manner. You should always acknowledge the
customer's concern, provide accurate information, avoid using technical jargon unless
necessary, and ensure the customer feels heard and valued. Always maintain a positive
tone and be patient. If you do not know the answer, say so honestly and suggest next steps.
Remember to be concise but thorough, professional but warm."""

user_message = "My order was supposed to arrive 3 days ago. What should I do?"

in1, out1, lat1 = call_and_measure(short_system, user_message, label="SHORT SYSTEM PROMPT")
in2, out2, lat2 = call_and_measure(long_system, user_message, label="LONG SYSTEM PROMPT")

print(f"\n=== COMPARISON ===")
print(f"Extra input tokens from longer system prompt: {in2 - in1}")
print(f"At 100,000 calls/month, that is {(in2 - in1) * 100000:,} extra input tokens")
print(f"At $0.59 per million tokens: ${(in2 - in1) * 100000 * 0.59 / 1_000_000:.2f} extra per month")
```

Run it. See the token difference between a tight system prompt and a bloated one, and what that costs at scale.

---

## Practical 2: Apply the 5 levers and measure the impact (12 min)

Add a new cell. Start with a costly baseline and progressively apply levers:

```python
# A realistic summarisation task
document = """
Customer: Hi, I purchased a wireless keyboard 2 months ago and the battery
started draining really fast. I charge it every day now but before it used
to last 2 weeks. I have tried resetting it and even bought new batteries but
nothing works. I'm frustrated because this was not cheap. I need this fixed
or replaced as soon as possible. My order number is KB-2024-8847.

Agent: Thank you for reaching out. I understand how frustrating that must be,
especially for a product you rely on daily. I have checked your order and you
are within our 12-month warranty period. I am raising a replacement request
now. You will receive a confirmation email within 2 hours and the replacement
will arrive in 3 to 5 business days. You do not need to return the faulty unit.
"""

task = "Summarise this support interaction."

# BASELINE: large model, no constraints
print("Running baseline...")
call_and_measure(
    system="You are a helpful assistant.",
    user=f"{task}\n\n{document}",
    model="llama-3.3-70b-versatile",
    label="BASELINE (70B, no constraints)"
)

# LEVER 2: limit output length
print("\nApplying Lever 2: limit output length...")
call_and_measure(
    system="You are a helpful assistant.",
    user=f"{task} Reply in exactly 2 sentences.\n\n{document}",
    model="llama-3.3-70b-versatile",
    label="LEVER 2: output length limited"
)

# LEVER 4: smaller model
print("\nApplying Lever 4: smaller model...")
call_and_measure(
    system="You are a helpful assistant.",
    user=f"{task} Reply in exactly 2 sentences.\n\n{document}",
    model="llama-3.1-8b-instant",
    label="LEVER 4: smaller model (8B)"
)
```

Run it. Compare token counts, latency, and reply quality across the three versions. For a simple summarisation task, the 8B model with a length constraint is often indistinguishable in quality from the 70B model with no constraint, at a fraction of the cost and time.

---

## Practical 3: Build a cost estimator for your own use case (8 min)

Add a new cell. Use what you have learned to estimate costs for a real scenario:

```python
def estimate_monthly_cost(
    system_prompt_words,
    avg_user_message_words,
    avg_reply_words,
    calls_per_day,
    input_price_per_million=0.59,   # Llama 3.3 70B on Groq (check current pricing)
    output_price_per_million=0.79
):
    # Convert words to tokens (1 word ~ 1.3 tokens)
    input_tokens = (system_prompt_words + avg_user_message_words) * 1.3
    output_tokens = avg_reply_words * 1.3

    calls_per_month = calls_per_day * 30

    input_cost = (input_tokens * calls_per_month * input_price_per_million) / 1_000_000
    output_cost = (output_tokens * calls_per_month * output_price_per_million) / 1_000_000
    total_cost = input_cost + output_cost

    print(f"\n=== COST ESTIMATE ===")
    print(f"Input tokens per call:  {input_tokens:.0f}")
    print(f"Output tokens per call: {output_tokens:.0f}")
    print(f"Calls per month:        {calls_per_month:,}")
    print(f"Input cost/month:       ${input_cost:.2f}")
    print(f"Output cost/month:      ${output_cost:.2f}")
    print(f"TOTAL COST/MONTH:       ${total_cost:.2f}")
    return total_cost

# Scenario 1: Internal FAQ chatbot (small company, 200 queries/day)
estimate_monthly_cost(
    system_prompt_words=150,
    avg_user_message_words=30,
    avg_reply_words=80,
    calls_per_day=200
)

# Scenario 2: Customer support bot (medium company, 5,000 queries/day)
estimate_monthly_cost(
    system_prompt_words=300,
    avg_user_message_words=60,
    avg_reply_words=120,
    calls_per_day=5000
)

# Scenario 3: Your own use case - replace the numbers below
estimate_monthly_cost(
    system_prompt_words=200,       # how long is your system prompt?
    avg_user_message_words=50,     # how long are typical user messages?
    avg_reply_words=100,           # how long are typical replies?
    calls_per_day=1000             # how many calls per day do you expect?
)
```

Run it. Change the numbers in Scenario 3 to match a real project you are thinking about. Get a real number before you build.

---

## What to show me after Chapter 10

You have completed the course. There is nothing more to show. There is only building.

Take one idea from any chapter and build something real with it. A classifier. A RAG pipeline. An eval set for something at work. An agent with one useful tool.

The concepts click differently when they are solving a real problem.
