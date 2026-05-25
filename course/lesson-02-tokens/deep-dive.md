# Deep dive: How tokenisation actually works

Optional reading. Skip if you just want to use AI. Read if you want to understand it.

---

## How the vocabulary was built

Before training, the engineers ran an algorithm called Byte Pair Encoding (BPE) on a massive text dataset.

It works like this:

1. Start with every individual character as its own token.
2. Find the two tokens that appear next to each other most often. Merge them into one new token.
3. Repeat until you have the vocabulary size you want (128,000 for Llama).

So common pairs like "th", "in", "er" became single tokens early. Then "the", "ing", "er" became tokens. Then common full words like "the", "and", "is" became tokens.

Rare words never made it to a single token. They are still represented by combining smaller pieces.

---

## Why non-English languages are more expensive

The training data was mostly English. So English words got compressed into single tokens efficiently.

Hindi, Tamil, Arabic, Japanese: far less training data, so the tokenizer never learned to compress these scripts efficiently.

A sentence in Hindi might use 3x as many tokens as the same sentence in English. More tokens means higher cost, slower response, and less room in the context window.

This is a real problem for AI products built for non-English markets. Some companies fine-tune their own tokenizers on local language data to fix this.

---

## Tokens and pricing in detail

Most APIs price input and output tokens differently.

Input tokens (what you send) are usually cheaper. Output tokens (what the model generates) cost more, because generating requires the model to actually run the prediction step for each token.

Rough example for a mid-range model:
- Input: $0.30 per million tokens
- Output: $0.60 per million tokens

So a reply costs twice as much per token as a question. If you want to reduce costs, ask for shorter replies.

---

## The context window is a sliding window, not a memory

When the conversation gets longer than the context window, the oldest messages get dropped. The model does not summarise them or store them somewhere. They are just gone.

Some applications handle this by:
1. Summarising old messages before they drop out ("so far we discussed X, Y, Z")
2. Storing important facts in a database and re-injecting them into the prompt when relevant
3. Asking the user to start a new conversation

This is one of the core engineering challenges in building AI products with long conversations. We cover it in Lesson 5 (RAG).

---

## Special tokens

Beyond regular text tokens, models have special tokens that mean specific things:

- `<|begin_of_text|>` marks the start of a new conversation
- `<|end_of_turn|>` marks the end of a user or assistant message
- `<|eot_id|>` signals the model to stop generating

You never type these. The API adds them automatically. But if you are ever inspecting raw model outputs or building at a lower level, you will see them.

---

## Why this matters for prompt engineering

Every character you add to your prompt costs tokens. A prompt that is 50 tokens longer costs more and takes up more context window.

This is why good prompt engineers are ruthless about cutting unnecessary words. Not just for clarity, but because bloated prompts have real costs at scale.
