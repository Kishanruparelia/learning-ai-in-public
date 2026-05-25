# Deep dive: What is actually happening under the hood

Optional reading. Skip if you just want to use AI. Read if you want to understand it.

---

## How the model was trained

Take a sentence from the internet. Hide the last word. Make the model guess.

Compare its guess to the real word. If wrong, adjust the 70 billion knobs slightly so next time it gets closer.

Do this trillions of times across the entire internet.

That is pretraining. It cost Meta an estimated $100M+ in compute to train Llama 3.3 70B. The model you are using for free.

---

## The architecture: Transformer

Every modern LLM is built on something called a Transformer. Introduced in a 2017 Google paper called "Attention is All You Need".

The key innovation is **attention**. When predicting the next word, the model does not just look at the previous word. It looks at every word in your input and decides which ones matter most for the current prediction.

That is why LLMs are good at long conversations. They can remember what you said 20 messages ago and weigh its importance.

Older AI (RNN, LSTM) struggled with this. They forgot context fast.

---

## What "next-token prediction" actually looks like

The model does not output a word. It outputs a probability for every possible word in its vocabulary (~128,000 options for Llama).

For "I will reach office by ___" it might compute:
- "10" = 18%
- "evening" = 14%
- "noon" = 9%
- "tomorrow" = 6%
- "submarine" = 0.0001%
- ...thousands more options

Then it samples one based on temperature.

---

## Temperature in detail

- **Temperature 0:** Always pick the highest probability word. Deterministic. Same answer every time.
- **Temperature 0.7:** Default in most APIs. Mostly picks likely words, occasionally picks something less likely. Good balance of useful and creative.
- **Temperature 1.5+:** Flattens the probability distribution. Even unlikely words get picked. Output becomes chaotic.

If you want a factual answer, use low temperature. If you want creative writing, use higher.

---

## Why Llama is free and ChatGPT is not

Meta released the Llama weights publicly. Anyone can download the 140GB file and run it.

Groq is a company that bought specialized chips (called LPUs) and runs Llama on them for free for small users. They make money from companies running it at scale.

OpenAI keeps GPT-4 weights secret. The only way to use it is through their API, which costs money per call.

Both approaches are valid. Open models give you control. Closed models often give you slightly better quality.

---

## How grammar works without rules

Nobody taught the model grammar.

But grammatically correct sentences appear far more often on the internet than grammatically wrong ones. So when the model learned "what word usually comes next", grammar emerged as a side effect.

This is also why LLMs sometimes write in the style of whatever they were trained on. If you ask for Shakespeare style, the model has seen enough Shakespeare to mimic the pattern.

---

## What this means for you

Every "smart" thing an AI does is built on this one trick: predict the next word, very well, very fast, with attention to context.

When you understand this, every other concept in this course (tokens, prompting, hallucinations, RAG, agents) becomes obvious. They are all just clever ways of feeding the prediction engine better inputs.
