# Lesson 1: What is an LLM

**Time needed:** 1 hour
**You will need:** A laptop, an internet connection, no coding experience

---

## What you will be able to do by the end

1. Explain what an LLM is to a friend in one sentence
2. Use ChatGPT and understand what is actually happening when you press enter
3. Run your first LLM call from your own laptop in 10 lines of code
4. Know why the same question can give two different answers

---

## The big idea

An LLM is a prediction engine. Nothing more.

You type words. It predicts the next word. Then the next. Then the next. That is the whole trick.

ChatGPT, Claude, Gemini, Llama, all of them do this one thing at massive scale.

---

## How it actually works (in plain English)

### 1. It is autocomplete on steroids

You know the suggested words above your phone keyboard? When you type "I will reach home by", it suggests "8" or "evening" or "tomorrow".

That is a tiny prediction engine. It learned from your last few thousand messages.

An LLM is the same idea. It learned from the entire internet instead. Wikipedia, Reddit, books, news, code, everything. Trillions of words.

So when you type "The capital of France is", it predicts "Paris" because in all the text it read, "Paris" almost always came after "The capital of France is".

### 2. Nobody programmed the answers

This is the part most people get wrong.

Nobody sat down and wrote rules like "if user asks about France, reply Paris". The model read billions of pages and figured out patterns on its own.

That is why it can talk about cricket, cooking, physics, and your favorite TV show in the same conversation. It has seen all of it.

### 3. It does not "know" things. It predicts what sounds right.

This is the most important mental shift in the whole course.

The LLM does not have a database it looks up. It generates text that statistically fits the pattern of what came before.

Usually the pattern matches the truth. Sometimes it does not. That gap is where AI makes things up. We will fix this in Lesson 4.

### 4. Same question, different answer

Ask ChatGPT the same question twice. You will get two slightly different replies.

That is because there is a randomness setting called **temperature**. Higher temperature, more random. Lower temperature, more predictable.

You will see this live in the practical section below.

---

## The two kinds of LLMs

### Closed models
Examples: ChatGPT (OpenAI), Claude (Anthropic), Gemini (Google).
You talk to them through a website or an app. You pay per use. You cannot see inside.

### Open models
Examples: Llama (Meta), Mistral, DeepSeek.
You can download them. You can run them on your own computer (if it is powerful enough). You can see how they were built.

For this course we will use **Llama 3.3 70B** through a service called **Groq**. Free. Fast. No credit card.

---

## What "70B" means

Llama 3.3 **70B** means 70 billion parameters.

A parameter is just a number inside the model. Picture 70 billion knobs, each tuned during training to get next-word prediction slightly better.

GPT-4 class models are estimated above 1 trillion knobs. More knobs usually means smarter model. But also slower and more expensive.

---

## Now go do the practical

Open `try-it-yourself.md` in this folder. Do not skip it. Reading without doing is how people fake-learn AI.

---

## Going deeper (optional)

If you want to understand what is actually happening under the hood, open `deep-dive.md`. Not required to move to Lesson 2.

---

## Check yourself

Open `test.md` and answer the 3 questions before moving on.
