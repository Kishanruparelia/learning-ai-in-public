# Try it yourself: Chapter 4

Three practicals. 30 minutes total. Do them in order.

---

## Practical 1: Trigger a factual and fabrication hallucination (10 min)

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
        temperature=0.7,
        messages=messages
    )
    print(f"\n--- {label} ---")
    print(response.choices[0].message.content)

# Type 1: Factual hallucination - asking for data the model cannot have
ask(
    "What was the exact closing price of Reliance Industries on NSE on 14th August 2023?",
    label="FACTUAL - NO FIX"
)

# Fix: tell it to admit uncertainty
ask(
    """What was the exact closing price of Reliance Industries on NSE on 14th August 2023?
If you do not have this data with certainty, say so explicitly instead of guessing.""",
    label="FACTUAL - WITH FIX"
)

# Type 2: Fabrication - asking for a specific regulatory reference
ask(
    "What is the exact SEBI circular number governing MTF eligibility for retail investors? Include the circular number, date, and relevant section.",
    label="FABRICATION - NO FIX"
)

# Fix: tell it not to invent, to suggest where to look instead
ask(
    """What is the exact SEBI circular number governing MTF eligibility for retail investors?
Important: Do not fabricate or guess circular numbers, dates, or sections.
If you are not certain, say so clearly and tell me where I can find the official source instead.""",
    label="FABRICATION - WITH FIX"
)
```

Run it. Read all four outputs carefully.

**What to look for:**
- Did the no-fix versions give you specific, confident-sounding answers?
- Did the fixed versions hedge appropriately and point you to a source?
- Notice how fluent and convincing the hallucinated outputs are. That is what makes them dangerous.

---

## Practical 2: Instruction and context hallucination (10 min)

Add a new cell and paste this:

```python
# Type 3: Instruction hallucination
# The rule "do not use the word opportunity" is buried in a long prompt

long_prompt = """We are launching a new SIP product at our brokerage.
Write a short message (2-3 sentences) for our relationship managers
to send to clients. The message should be about our new product launch.
Make sure it sounds professional. Do not use jargon. Keep it simple.
Do not use the word opportunity. The message should encourage clients
to ask their RM for more details. Friendly tone."""

ask(long_prompt, label="INSTRUCTION - NO FIX")

# Fix: move the critical rule to the system prompt
ask(
    """We are launching a new SIP product. Write a 2-3 sentence message for RMs
to send to clients. Professional, simple, friendly. Encourage clients to ask their RM for details.""",
    system="CRITICAL RULE: Never use the word 'opportunity' in any output.",
    label="INSTRUCTION - WITH FIX"
)

# Check if "opportunity" appeared
print("\n--- CHECKING FOR 'opportunity' ---")
print("(Read the outputs above and check manually)")


# Type 4: Context hallucination
# Unusual portfolio data that the model might 'normalise'

portfolio_note = """
Client: Mr. Sharma
Portfolio allocation:
- Commodities: 80%
- Equity: 15%
- Fixed Deposit: 5%
"""

ask(
    f"Write a 2-line summary of this client's portfolio:\n{portfolio_note}",
    label="CONTEXT - NO FIX"
)

# Fix: ground it explicitly
ask(
    f"""Write a 2-line summary of this client's portfolio.
RULES: Use ONLY the information provided below. Do not add anything from your general knowledge.
Quote the exact percentages as given. Do not reframe or interpret the allocation.

{portfolio_note}""",
    label="CONTEXT - WITH FIX"
)
```

Run it. For the instruction test, check whether the word "opportunity" appears in each version. For the context test, see if the no-fix version softens or reframes the 80% commodities allocation.

---

## Practical 3: Logical hallucination and chain of thought fix (10 min)

Add a new cell and paste this:

```python
# Type 5: Logical hallucination - multi-step maths without working shown
ask(
    """A client has Rs 5,00,000 in Stock A which went up 12%,
and Rs 3,00,000 in Stock B which went down 8% over 6 months.
What is the total profit or loss in rupees, and what is the
portfolio return percentage? Give me just the final numbers.""",
    label="LOGICAL - NO FIX"
)

# Fix: chain of thought with explicit steps
ask(
    """A client has Rs 5,00,000 in Stock A which went up 12%,
and Rs 3,00,000 in Stock B which went down 8% over 6 months.
What is the total profit or loss in rupees and portfolio return percentage?

Work through each step:
1. Calculate profit or loss on Stock A in rupees
2. Calculate profit or loss on Stock B in rupees
3. Calculate total net profit or loss
4. State total amount invested
5. Calculate portfolio return as a percentage
6. State the final answer clearly""",
    label="LOGICAL - WITH FIX"
)

# The correct answer
print("\n--- CORRECT ANSWER ---")
print("Stock A: Rs 5,00,000 x 12% = +Rs 60,000")
print("Stock B: Rs 3,00,000 x 8% = -Rs 24,000")
print("Net profit: Rs 36,000")
print("Total invested: Rs 8,00,000")
print("Portfolio return: 36,000 / 8,00,000 = 4.5%")
```

Run it. Compare the no-fix answer against the correct answer. Then see if the chain of thought version lands on 4.5%.

---

## What to show me before moving to Chapter 5

1. A screenshot showing one hallucinated output and its fixed version
2. A one-line answer to: "Why is a hallucination more dangerous than an AI simply saying I don't know?"
