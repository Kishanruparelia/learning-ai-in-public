# Try it yourself: Lesson 2

Three practicals. 30 minutes total. Do them in order.

---

## Practical 1: Watch your words become tokens (10 min)

Go to this link: **tiktokenizer.vercel.app**

You will see a text box on the left and coloured highlights on the right. Every colour is one token.

Try these one at a time. Paste each into the box and count the tokens shown at the top.

**Test 1:** Type your own name. Notice whether it is 1 token or splits into 2.

**Test 2:** Paste this sentence:
```
I want to open a demat account
```
Count the tokens. You should see around 9.

**Test 3:** Paste this:
```
I want to open a dematerialised account for equity trading on NSE
```
Count the tokens. Notice "dematerialised" splits into multiple tokens because it is a long, less common word.

**Test 4:** Paste a number like `10000000`. Notice every digit becomes its own token. A number with 8 digits is 8 tokens.

**Test 5:** Type a Hindi or Marathi word in English letters, like `namaste` or `dhanyawad`. Then try typing the same word in Devanagari script. Notice Devanagari uses far more tokens per word than English. We come back to why this matters in the deep-dive.

**What to notice:** Short common English words are almost always 1 token. Long words, numbers, and non-English scripts use more tokens per concept.

---

## Practical 2: Estimate cost before you build (10 min)

This is a skill every AI product builder needs. Before you build anything, estimate the token usage so you are not surprised by the bill.

Scenario: You are building an AI customer service bot for a brokerage. Each conversation looks like this:

- System prompt (instructions to the AI): 200 words
- Customer message: 50 words
- AI reply: 100 words

**Step 1:** Estimate tokens for one conversation.

Using the rule of thumb (1 word is roughly 1.3 tokens):
- System prompt: 200 x 1.3 = 260 tokens
- Customer message: 50 x 1.3 = 65 tokens
- AI reply: 100 x 1.3 = 130 tokens
- Total per conversation: roughly 455 tokens

**Step 2:** Scale it up.

If the bot handles 500 conversations a day:
- 455 x 500 = 227,500 tokens per day
- 227,500 x 30 = 6,825,000 tokens per month

**Step 3:** Price it.

Llama 3.3 70B via Groq is free for low volume. If you scaled to a paid model at $0.30 per million tokens:
- 6,825,000 / 1,000,000 x $0.30 = $2.05 per month

That is the actual cost of running an AI customer service bot at 500 conversations a day. Under $3 a month.

Now try your own scenario. Pick any AI usecase you can think of, estimate message sizes, and calculate a monthly token budget.

---

## Practical 3: See the context window in action (10 min)

Open colab.research.google.com and create a new notebook. Paste this code and run it with Shift + Enter:

```python
# Install Groq
!pip install groq -q

from groq import Groq
from google.colab import userdata

client = Groq(api_key=userdata.get("GROQ_API_KEY"))

# We will build a conversation that grows with each message
# and watch the model remember (then eventually forget) earlier context

conversation = [
    {"role": "user", "content": "My name is Rahul and I work at a brokerage in Mumbai."},
]

# Get first reply
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=conversation
)

reply = response.choices[0].message.content
print("AI:", reply)

# Add the reply to conversation history
conversation.append({"role": "assistant", "content": reply})

# Now ask a follow-up that requires memory
conversation.append({"role": "user", "content": "What city do I work in?"})

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=conversation
)

print("\nAI:", response.choices[0].message.content)
```

Run it. The AI should correctly say Mumbai, because the full conversation history was passed in the second call.

Now try a version without history. Add a new cell and paste:

```python
# This time, we do NOT pass the conversation history
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "What city do I work in?"}
    ]
)

print("AI (no memory):", response.choices[0].message.content)
```

Run it. The AI now has no idea. It will either say it does not know or make something up.

**What this proves:** the model has no memory of its own. You are responsible for passing the history. The context window is the only memory it has.

---

## What to show me before moving to Lesson 3

1. A screenshot of Tiktokenizer showing your own name tokenised
2. A one-line answer to: "Why did the AI forget the city when you did not pass the history?"
