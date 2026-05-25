# Try it yourself: Chapter 3

Three practicals. 30 minutes total. Do them in order.

---

## Practical 1: Weak vs strong prompt, side by side (10 min)

Open colab.research.google.com and create a new notebook. Paste and run this:

```python
!pip install groq -q
from groq import Groq
from google.colab import userdata

client = Groq(api_key=userdata.get("GROQ_API_KEY"))

def ask(prompt, label=""):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}]
    )
    print(f"\n--- {label} ---")
    print(response.choices[0].message.content)

# Weak prompt
ask(
    "Write an email to a client",
    label="WEAK"
)

# Strong prompt using Role + Task + Format + Constraints
ask(
    """You are a relationship manager at SBI Securities.
Write a re-engagement email to a client named Ankit who has not logged
into his trading account in 45 days.

Rules:
- Subject line + email body
- Maximum 5 sentences in the body
- Mention that markets have been active
- End with one specific call to action
- Professional but warm tone""",
    label="STRONG"
)
```

Run it. Read both outputs. The weak prompt will give you a generic template. The strong one will give you something you could actually send.

**What to notice:** The model did not become smarter. You gave it better instructions.

---

## Practical 2: Add a few-shot example and watch consistency improve (10 min)

Add a new cell and paste this:

```python
# WITHOUT an example - output format will vary
ask(
    """Classify this customer support message as one of:
ACCOUNT_ISSUE, TRADE_ISSUE, PAYMENT_ISSUE, or GENERAL_QUERY

Message: "My sell order went through but the shares are still showing in my portfolio."
""",
    label="NO EXAMPLE"
)

# WITH one example - output format becomes predictable
ask(
    """Classify customer support messages into one of these categories:
ACCOUNT_ISSUE, TRADE_ISSUE, PAYMENT_ISSUE, GENERAL_QUERY

Example:
Message: "I cannot log into my account since yesterday."
Category: ACCOUNT_ISSUE
Reason: Login and access problems are account issues.

Now classify this:
Message: "My sell order went through but the shares are still showing in my portfolio."
Category:""",
    label="WITH EXAMPLE"
)
```

Run it. The no-example version might give you a paragraph of explanation. The with-example version should give you a clean one-line category, matching the format you showed it.

**What to notice:** One example taught the model your exact output format. This is how you make AI outputs predictable enough to plug into a real system.

---

## Practical 3: Chain of thought on a real calculation (10 min)

Add a new cell and paste this:

```python
# Without chain of thought - often wrong on multi-step problems
ask(
    """A client invested Rs 4,00,000 in Fund A (up 15%) and Rs 6,00,000
in Fund B (down 5%). What is the overall portfolio return percentage?
Give me just the final number.""",
    label="NO CHAIN OF THOUGHT"
)

# With chain of thought - forces the model to show its working
ask(
    """A client invested Rs 4,00,000 in Fund A (up 15%) and Rs 6,00,000
in Fund B (down 5%). What is the overall portfolio return percentage?

Work through it step by step:
1. Calculate profit or loss on Fund A in rupees
2. Calculate profit or loss on Fund B in rupees
3. Calculate net profit or loss
4. Divide net profit or loss by total invested
5. State the final percentage return""",
    label="WITH CHAIN OF THOUGHT"
)

# The correct answer for reference:
# Fund A: 4,00,000 x 15% = +60,000
# Fund B: 6,00,000 x 5% = -30,000
# Net: +30,000
# Total invested: 10,00,000
# Return: 30,000 / 10,00,000 = 3%
print("\n--- CORRECT ANSWER ---")
print("Fund A: +Rs 60,000 | Fund B: -Rs 30,000 | Net: +Rs 30,000 | Return: 3%")
```

Run it. Check whether the no-chain-of-thought version got 3% or made a mistake. The chain of thought version should walk through each step and land on 3%.

**What to notice:** The model is not bad at maths. It is bad at skipping steps. Force the steps, get the right answer.

---

## What to show me before moving to Chapter 4

1. A screenshot showing the weak vs strong email outputs side by side
2. A one-line answer to: "What is the difference between a few-shot example and a constraint in a prompt?"
