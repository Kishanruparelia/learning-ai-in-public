# Try it yourself: Chapter 8

Three practicals. 30 minutes total. Do them in order.

---

## Practical 1: Exact match eval for a classification task (8 min)

Open colab.research.google.com and create a new notebook. Paste and run this:

```python
!pip install groq -q
from groq import Groq
from google.colab import userdata

client = Groq(api_key=userdata.get("GROQ_API_KEY"))

def classify(message, system=""):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": message})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=messages
    )
    return response.choices[0].message.content.strip()

# --- EVAL SET ---
# Each item has an input and the correct expected answer
eval_set = [
    {"input": "My order has not arrived after 2 weeks.", "expected": "COMPLAINT"},
    {"input": "What are your delivery timeframes?",       "expected": "QUERY"},
    {"input": "Your team was incredibly helpful, thank you!", "expected": "COMPLIMENT"},
    {"input": "I was charged twice for the same item.",   "expected": "COMPLAINT"},
    {"input": "Do you offer international shipping?",     "expected": "QUERY"},
    {"input": "Best customer service I have ever had.",   "expected": "COMPLIMENT"},
    {"input": "The product broke after one day.",         "expected": "COMPLAINT"},
    {"input": "How do I track my order?",                 "expected": "QUERY"},
]

# --- WEAK PROMPT ---
weak_prompt = "Classify this customer message as COMPLAINT, QUERY, or COMPLIMENT. Reply with only the category word."

# --- RUN EVAL ---
def run_eval(prompt, eval_set, label):
    correct = 0
    print(f"\n=== {label} ===")
    for item in eval_set:
        result = classify(item["input"], system=prompt)
        passed = result.upper() == item["expected"]
        correct += passed
        status = "PASS" if passed else f"FAIL (got: {result})"
        print(f"  {status} | {item['input'][:50]}")
    score = correct / len(eval_set) * 100
    print(f"\nScore: {correct}/{len(eval_set)} = {score:.0f}%")
    return score

score_weak = run_eval(weak_prompt, eval_set, "WEAK PROMPT")
```

Run it. You will see a score out of 100% showing how many classifications were correct.

Now add a new cell with a stronger prompt and compare:

```python
# --- STRONGER PROMPT ---
strong_prompt = """You are a customer support triage assistant.
Classify the customer message into exactly one of these categories:
COMPLAINT - the customer is unhappy, reporting a problem, or expressing frustration
QUERY - the customer is asking a question or requesting information
COMPLIMENT - the customer is expressing satisfaction or gratitude

Reply with only the single category word in capitals. No explanation."""

score_strong = run_eval(strong_prompt, eval_set, "STRONG PROMPT")

print(f"\nImprovement: {score_strong - score_weak:.0f} percentage points")
```

Run it. See if the stronger prompt gets a better score. This is the eval loop in action.

---

## Practical 2: LLM-as-a-judge for open-ended text (12 min)

Add a new cell. Now you will evaluate open-ended replies where there is no single right answer:

```python
import json

# The task: write a helpful reply to a customer complaint
complaint = "I ordered a laptop stand 3 weeks ago and it still has not arrived. I need it urgently for work. This is unacceptable."

# Two versions of a customer reply to evaluate
reply_a = """I apologise for the delay with your laptop stand order. Please contact our support team at support@example.com with your order number and we will investigate and resolve this as quickly as possible."""

reply_b = """I completely understand how frustrating this must be, especially when you need it for work. I am sorry for the delay.

Here is what I will do right now:
1. Check your order status and flag it as urgent
2. If it has not shipped, we will express ship a replacement today
3. If it is in transit, I will get you the exact delivery date

Can you share your order number so I can look into this immediately?"""

def judge_reply(question, reply, label):
    judge_prompt = f"""You are an evaluator assessing the quality of a customer service reply.

CUSTOMER MESSAGE: {question}

REPLY TO EVALUATE: {reply}

Score this reply from 1 to 5 on each dimension:
- empathy: does it acknowledge the customer's frustration genuinely?
- helpfulness: does it offer a concrete next step or solution?
- clarity: is it easy to understand with no jargon?

Return ONLY valid JSON in this exact format:
{{"empathy": 0, "helpfulness": 0, "clarity": 0, "reasoning": "one sentence"}}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[{"role": "user", "content": judge_prompt}]
    )

    raw = response.choices[0].message.content.strip()

    # Extract JSON from the response
    start = raw.find("{")
    end = raw.rfind("}") + 1
    scores = json.loads(raw[start:end])
    total = scores["empathy"] + scores["helpfulness"] + scores["clarity"]

    print(f"\n--- {label} ---")
    print(f"Empathy: {scores['empathy']}/5 | Helpfulness: {scores['helpfulness']}/5 | Clarity: {scores['clarity']}/5")
    print(f"Total: {total}/15")
    print(f"Reasoning: {scores['reasoning']}")
    return total

score_a = judge_reply(complaint, reply_a, "REPLY A")
score_b = judge_reply(complaint, reply_b, "REPLY B")

print(f"\nWinner: {'Reply B' if score_b > score_a else 'Reply A'} ({max(score_a, score_b)}/15 vs {min(score_a, score_b)}/15)")
```

Run it. The LLM judge will score both replies across 3 dimensions and explain its reasoning.

**What to notice:** You are using one LLM to evaluate the output of another. This scales. You can run this across hundreds of examples automatically, which would take hours if done by hand.

---

## Practical 3: Build your own eval set (10 min)

Add a new cell. Write a 5-item eval set for a task of your choice:

```python
# Choose a task and write 5 test cases
# Examples: email subject line quality, FAQ answer accuracy,
#           sentiment detection, summary completeness

my_task_description = """
[DESCRIBE YOUR TASK HERE - e.g. "Classify support tickets into: BILLING, TECHNICAL, ACCOUNT, or OTHER"]
"""

my_eval_set = [
    {"input": "[TEST INPUT 1]", "expected": "[EXPECTED OUTPUT 1]"},
    {"input": "[TEST INPUT 2]", "expected": "[EXPECTED OUTPUT 2]"},
    {"input": "[TEST INPUT 3]", "expected": "[EXPECTED OUTPUT 3]"},
    {"input": "[TEST INPUT 4]", "expected": "[EXPECTED OUTPUT 4]"},
    {"input": "[TEST INPUT 5]", "expected": "[EXPECTED OUTPUT 5]"},
]

my_prompt = """
[WRITE YOUR SYSTEM PROMPT HERE]
"""

# Run your eval
run_eval(my_prompt, my_eval_set, "MY EVAL")
```

Replace the placeholders with your own task, test cases, and prompt. Run it. Then tweak the prompt and run again until the score improves.

---

## What to show me before moving to Chapter 9

1. A screenshot showing the score difference between weak and strong prompt in Practical 1
2. A one-line answer to: "Why is LLM-as-a-judge useful for open-ended tasks where exact matching does not work?"
