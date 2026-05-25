# Chapter 5: System Prompts

**Time needed:** 1 hour
**You will need:** A browser, your Groq API key, Google Colab open

---

## What you will be able to do by the end

1. Explain what a system prompt is and how it differs from a user prompt
2. Write a system prompt that shapes the model's persona, rules, and output style
3. Know what belongs in a system prompt vs what belongs in the user message
4. Build a simple AI assistant with a fixed identity using just a system prompt

---

## The big idea

Every AI product you have ever used has a system prompt behind it.

When you talk to a bank's chatbot and it stays on topic, does not give investment advice, and always ends with "please speak to your relationship manager," that behaviour comes from a system prompt.

When ChatGPT refuses to help with certain requests, that is a system prompt.

When an RM co-pilot always formats its replies as bullet points and never uses jargon, that is a system prompt.

The system prompt is the developer's layer. It sets the rules before the user ever types a word.

---

## What a system prompt is

A system prompt is a set of instructions passed to the model before the conversation starts.

The user does not see it. It does not appear in the chat. But it shapes every single reply the model gives.

In code, it looks like this:

```python
messages = [
    {"role": "system", "content": "You are a helpful RM assistant at SBI Securities."},
    {"role": "user", "content": "What is a demat account?"}
]
```

The `system` role message is the system prompt. The `user` role message is what the user typed.

---

## What goes in a system prompt

Think of the system prompt as the briefing you give a new hire on their first day. Everything they need to know before they take their first call.

### 1. Persona
Who is the model playing?

```
You are Maya, a customer service assistant at SBI Securities.
You are helpful, patient, and speak in simple English.
You never use financial jargon without explaining it.
```

### 2. Scope
What is it allowed to talk about? What is off limits?

```
You only answer questions related to demat accounts, trading, and SBI Securities products.
If the user asks about competitors, other banks, or unrelated topics, politely redirect them.
```

### 3. Rules and guardrails
What must it always or never do?

```
Never give specific buy or sell recommendations.
Always recommend the user speak to a registered investment advisor for personalized advice.
Never share information about other clients.
If the user seems distressed or mentions financial loss, respond with empathy before information.
```

### 4. Output format
How should replies be structured?

```
Keep all replies under 4 sentences unless the user asks for more detail.
Use simple numbered lists when explaining steps.
Always end with one follow-up question to confirm the user's need was met.
```

### 5. Context about the world it operates in
Background the model needs but the user does not need to repeat every message.

```
SBI Securities is the broking arm of State Bank of India.
Our products include equity trading, IPO applications, mutual funds, and MTF.
Our support hours are 9am to 6pm IST, Monday to Friday.
```

---

## System prompt vs user prompt: what goes where

| Belongs in system prompt | Belongs in user message |
|--------------------------|------------------------|
| Persona and identity | The user's actual question |
| Permanent rules and guardrails | Any data specific to this request |
| Output format preferences | Follow-up instructions |
| Background context about the product | |
| Critical rules (never do X) | |

A common mistake is putting rules in the user message every time. If the rule applies to every conversation, it belongs in the system prompt. If the rule only applies to this specific request, it belongs in the user message.

---

## System prompts persist across the conversation

The system prompt is included with every API call. The user does not need to re-state the rules.

This is why a well-built AI assistant feels consistent. The persona, tone, and guardrails apply to every reply, no matter how long the conversation gets.

The one exception: if the conversation grows very long and approaches the context window limit, the system prompt is always kept. The oldest user and assistant messages get dropped first. The system prompt is protected.

---

## A real example: SBI Securities RM Co-Pilot

Here is what a system prompt for an RM assistant might look like:

```
You are Arjun, an AI co-pilot for relationship managers at SBI Securities.

Your job is to help RMs prepare for client conversations, draft messages,
and quickly look up product information. You do not talk to clients directly.

RULES:
- Never give specific investment advice or price targets
- Always cite which product category a recommendation falls under
- If asked about a competitor product, acknowledge it neutrally and pivot
  to the equivalent SBI Securities offering
- Keep all draft messages under 5 sentences unless asked for more
- Use professional but warm language. Not corporate, not casual.

CONTEXT:
- RMs manage HNI and retail clients with portfolios from Rs 5 lakh to Rs 5 crore
- Key products: equity, MF, IPO, MTF, bonds
- Current campaign: SIP upsell for clients with idle cash above Rs 2 lakh

OUTPUT FORMAT:
- When drafting a client message, always label it "DRAFT:" at the top
- When giving product information, use bullet points
- When you are not sure about a fact, say "Please verify this before sharing with the client"
```

That system prompt turns a general LLM into a focused, safe, on-brand tool for one specific job.

---

## Now go do the practical

Open `try-it-yourself.md`. You will build two versions of the same assistant, one with a weak system prompt and one with a strong one, and see how differently they behave.

---

## Going deeper (optional)

Open `deep-dive.md` to understand how system prompts interact with jailbreaks, how much you can trust them as guardrails, and what prompt injection means for system prompt security.

---

## Check yourself

Open `test.md` before moving to Chapter 6.
