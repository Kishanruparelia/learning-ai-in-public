# Lesson 2: Tokens

**Time needed:** 1 hour
**You will need:** A browser, the Groq API key from Lesson 1

---

## What you will be able to do by the end

1. Explain what a token is and why it is not the same as a word
2. Estimate the token count of any text before sending it to an AI
3. Understand why AI has a memory limit and what happens when you hit it
4. Know why longer prompts cost more money

---

## The big idea

Every LLM thinks in tokens, not words.

Before your message even reaches the model, it gets chopped into small pieces. Those pieces are tokens. The model reads tokens, thinks in tokens, and replies in tokens.

If you do not understand tokens, you will be confused when the AI cuts off mid-sentence, forgets what you said earlier, or your bill is higher than expected. This lesson fixes all of that.

---

## What is a token

A token is not a word. It is not a character either. It is somewhere in between.

Here are real examples of how the sentence "I love playing cricket" gets split:

| Text | Tokens |
|------|--------|
| I | 1 token |
| love | 1 token |
| playing | 1 token |
| cricket | 1 token |

Simple common words are usually 1 token. But longer or rarer words split differently:

| Text | Tokens |
|------|--------|
| Hallucination | 3 tokens: "Hall", "ucin", "ation" |
| Unconstitutional | 5 tokens |
| Mumbai | 2 tokens: "Mum", "bai" |
| 1000000 | 7 tokens (each digit is separate) |

The rough rule of thumb: **1 token is about 4 characters, or about 0.75 words**.

So 100 words is roughly 133 tokens. 1000 words is roughly 1300 tokens.

---

## Why tokens exist

The model did not learn from words. It learned from patterns in chunks of text.

During training, the engineers built a vocabulary of about 128,000 common chunks. Common words got their own token. Rare words got split into smaller chunks that do exist in the vocabulary.

This way, the model can handle any word in any language, even made-up words, because it can always break them into smaller pieces it has seen before.

---

## Why tokens matter to you

### 1. Cost

Every API charges per token. Not per message, not per word. Per token.

Typical pricing for a mid-range model today: around $0.30 per million input tokens.

Send a 500-word prompt, get a 200-word reply. That is roughly 650 tokens in + 267 tokens out = 917 tokens total. About $0.0003. Tiny.

But if you are running this for 10,000 users a day, the numbers scale fast.

### 2. Context window

Every model has a limit on how many tokens it can hold in memory at once. This is called the context window.

Llama 3.3 70B has a context window of 128,000 tokens. That sounds huge. It is roughly 100,000 words, or about 300 pages of text.

But here is what fills it fast:
- Your system prompt
- The entire conversation history so far
- Any documents you paste in
- The model's reply

Once you hit the limit, the model starts forgetting the oldest parts of the conversation. That is why a very long chat session sometimes feels like the AI forgot what you told it an hour ago.

### 3. Speed

Models generate one token at a time. A 200-token reply takes roughly twice as long as a 100-token reply.

If you want faster responses, ask for shorter ones.

---

## The context window in real numbers

| What you send | Approximate tokens |
|---------------|-------------------|
| A typical WhatsApp message | 20 to 50 |
| A one-page email | 300 to 500 |
| A 10-page report | 3,000 to 5,000 |
| An entire novel (Harry Potter book 1) | ~180,000 |
| Llama 3.3 70B context window | 128,000 |

So you can fit most business documents easily. You cannot fit a full novel in one shot.

---

## Now go do the practical

Open `try-it-yourself.md`. You will use a tool called Tiktokenizer to see exactly how your own words get split into tokens, live, in your browser. No code required.

---

## Going deeper (optional)

Open `deep-dive.md` to understand how the tokenizer vocabulary was built and why some languages are more expensive than others.

---

## Check yourself

Open `test.md` before moving to Lesson 3.
