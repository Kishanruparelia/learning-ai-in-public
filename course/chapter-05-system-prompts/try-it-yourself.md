# Try it yourself: Chapter 5

Three practicals. 30 minutes total. Do them in order.

---

## Practical 1: Weak system prompt vs strong system prompt (10 min)

Open colab.research.google.com and create a new notebook. Paste and run this:

```python
!pip install groq -q
from groq import Groq
from google.colab import userdata

client = Groq(api_key=userdata.get("GROQ_API_KEY"))

def ask_with_system(system, user, label=""):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    )
    print(f"\n--- {label} ---")
    print(response.choices[0].message.content)

# Same user question, two very different system prompts
user_question = "Should I invest in small cap funds right now?"

# Weak system prompt - generic, no rules
ask_with_system(
    system="You are a helpful assistant.",
    user=user_question,
    label="WEAK SYSTEM PROMPT"
)

# Strong system prompt - persona, scope, rules, format
ask_with_system(
    system="""You are Arjun, an AI assistant for relationship managers at SBI Securities.

RULES:
- Never give specific buy, sell, or hold recommendations
- Never tell a client whether NOW is a good time to invest in any asset
- Always recommend the user speak to their RM for personalised advice
- If asked for a market opinion, explain the category neutrally and redirect

OUTPUT:
- Keep replies under 4 sentences
- End every reply with: "Would you like me to connect you with your RM for personalised guidance?" """,
    user=user_question,
    label="STRONG SYSTEM PROMPT"
)
```

Run it. The weak version will likely give investment opinions. The strong version should stay within guardrails and redirect.

**What to notice:** Same model. Same question. Completely different behaviour. The system prompt is the product.

---

## Practical 2: Test the guardrails (10 min)

Add a new cell. Now you will try to push the assistant off its rails with tricky questions:

```python
strong_system = """You are Maya, a customer service assistant at SBI Securities.

SCOPE: Only answer questions about SBI Securities products and services.
If the user asks about competitors, politics, sports, or anything unrelated,
politely say you can only help with SBI Securities topics.

RULES:
- Never mention competitor names positively or negatively
- Never give investment advice or price predictions
- If the user seems frustrated, acknowledge it before answering

OUTPUT: Keep replies under 3 sentences. Professional and warm."""

# Test 1: In-scope question
ask_with_system(
    system=strong_system,
    user="How do I apply for an IPO through SBI Securities?",
    label="IN-SCOPE QUESTION"
)

# Test 2: Out-of-scope question
ask_with_system(
    system=strong_system,
    user="Who do you think will win the IPL this year?",
    label="OUT-OF-SCOPE QUESTION"
)

# Test 3: Competitor question
ask_with_system(
    system=strong_system,
    user="Is Zerodha better than SBI Securities for equity trading?",
    label="COMPETITOR QUESTION"
)

# Test 4: Emotional user
ask_with_system(
    system=strong_system,
    user="I lost Rs 50,000 in the market today because of bad advice. I am furious.",
    label="EMOTIONAL USER"
)
```

Run all four. Check:
- Did the assistant stay on scope for the IPL question?
- Did it handle the competitor question without slamming Zerodha or praising it?
- Did it acknowledge the emotional user's frustration before jumping to information?

---

## Practical 3: Build your own assistant (10 min)

Now write your own system prompt from scratch. Pick one of these scenarios (or make up your own):

**Option A:** An AI assistant for SBI Securities new account opening team. It helps people understand the KYC process, what documents are needed, and what to expect after applying. It cannot access account data.

**Option B:** An AI co-pilot for SBI Securities research analysts. It helps draft earnings summaries and format data, but never makes stock calls.

**Option C:** An internal HR bot for SBI Securities employees. It answers questions about leave policy, payroll dates, and benefits. It does not handle complaints or performance discussions.

Add a new cell and write it:

```python
# Write your own system prompt here
my_system_prompt = """
[YOUR SYSTEM PROMPT HERE]
"""

# Test it with 3 questions: one in-scope, one edge case, one out-of-scope
ask_with_system(
    system=my_system_prompt,
    user="[YOUR IN-SCOPE TEST QUESTION]",
    label="MY ASSISTANT - IN SCOPE"
)

ask_with_system(
    system=my_system_prompt,
    user="[YOUR EDGE CASE QUESTION]",
    label="MY ASSISTANT - EDGE CASE"
)

ask_with_system(
    system=my_system_prompt,
    user="[YOUR OUT OF SCOPE QUESTION]",
    label="MY ASSISTANT - OUT OF SCOPE"
)
```

Replace the placeholders and run it. Adjust your system prompt until all three tests behave the way you want.

---

## What to show me before moving to Chapter 6

1. A screenshot of the weak vs strong system prompt outputs for the small cap funds question
2. The system prompt you wrote in Practical 3 (paste it as text)
