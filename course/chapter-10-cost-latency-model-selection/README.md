# Chapter 10: Cost, Latency, and Model Selection

**Time needed:** 1 hour
**You will need:** A browser, your Groq API key, Google Colab open

---

## What you will be able to do by the end

1. Estimate the cost of running any AI feature before building it
2. Understand what drives latency and how to reduce it
3. Choose the right model for a given task using a simple framework
4. Know the 5 levers you can pull to reduce cost and latency without hurting quality

---

## The big idea

A demo that works is easy to build. A product that works at scale without breaking the budget or making users wait is the real engineering challenge.

Cost and latency are not afterthoughts. They determine whether a feature is viable. An AI feature that costs $10 per user per month is a different product from one that costs $0.02. One of them ships. One of them stays on a whiteboard.

---

## What drives cost

Every API call costs money based on two things: input tokens and output tokens.

**Input tokens:** Everything you send to the model. Your system prompt, the conversation history, any documents you paste in, the user's message.

**Output tokens:** Everything the model sends back. The reply.

Output tokens typically cost 2x to 3x more than input tokens because generating each token requires a full forward pass through the model.

### The cost formula

```
Cost = (input tokens × input price) + (output tokens × output price)
```

Example with a mid-range model at $0.30 per million input tokens and $0.60 per million output tokens:

- System prompt: 300 tokens
- User message: 50 tokens
- Model reply: 150 tokens
- Total: 350 input + 150 output
- Cost: (350 × 0.30 / 1,000,000) + (150 × 0.60 / 1,000,000) = $0.000105 + $0.000090 = $0.000195 per call

That is under $0.0002 per call. At 10,000 calls per day: $2 per day, $60 per month.

At 1,000,000 calls per day: $195 per day, $5,850 per month.

Scale is where cost becomes a real decision.

---

## What drives latency

Latency is the time from when you send a request to when the model finishes replying.

It has two parts:

**Time to first token (TTFT):** How long before the first word appears. Driven by model size and server load.

**Time to complete (TTC):** How long to finish the full reply. Driven by the number of output tokens.

The model generates tokens at a certain speed (tokens per second). A 500-token reply takes 5x longer than a 100-token reply at the same speed.

Groq's LPU hardware is specifically designed to maximise tokens per second. That is why Llama 3.3 70B on Groq feels faster than on standard GPU infrastructure.

---

## The model selection framework

Not every task needs the most powerful model. Matching model capability to task complexity saves cost and latency.

Think of models in three tiers:

**Tier 1: Small, fast, cheap**
Examples: Llama 3.1 8B, Gemini Flash, GPT-4o mini
Good for: classification, simple extraction, routing, short-form generation
Cost: 10x to 50x cheaper than top models
Latency: very fast

**Tier 2: Mid-range, balanced**
Examples: Llama 3.3 70B, Claude Haiku, Gemini Pro
Good for: summarisation, RAG answers, drafting, moderate reasoning
Cost: moderate
Latency: fast to moderate

**Tier 3: Large, powerful, expensive**
Examples: GPT-4o, Claude Opus, Gemini Ultra
Good for: complex reasoning, code generation, nuanced long-form writing
Cost: 10x to 100x more than Tier 1
Latency: slower

The decision rule: use the smallest model that gets the job done at your quality threshold. Test with your eval set from Chapter 8.

---

## The 5 levers for reducing cost and latency

### Lever 1: Shorter system prompts
Every word in your system prompt costs tokens on every single API call. A 1,000-word system prompt that could be 200 words wastes 800 tokens per call. At 100,000 calls per month that is 80 million extra tokens.

Audit your system prompt. Remove anything the model does not actually need.

### Lever 2: Limit output length
Tell the model explicitly how long to be. "Reply in 2 sentences" is not just a style choice. It cuts output tokens by 80%, which cuts cost and latency proportionally.

```
Keep your reply under 3 sentences.
```

### Lever 3: Cache repeated inputs
If your system prompt is the same for every call, many APIs support prompt caching. The first call processes the system prompt fully. Subsequent calls with the same system prompt reuse a cached version at a fraction of the cost.

Anthropic, OpenAI, and Groq all support some form of caching. Check the docs for the model you are using.

### Lever 4: Use a smaller model for simple tasks
Route simple requests (classification, short answers, yes/no decisions) to a small cheap model. Only send complex requests to the large expensive model.

This is called model routing. A well-designed routing layer can cut costs by 60 to 80% with no visible quality drop for the majority of requests.

### Lever 5: Reduce conversation history
Every message in the conversation history adds tokens to every subsequent call. A 20-turn conversation can have 3,000+ tokens of history.

Strategies:
- Summarise old turns instead of keeping them verbatim
- Only keep the last N turns in the prompt
- Extract key facts from the history and store them compactly

---

## A practical cost comparison

Same task (summarise a support ticket) across model tiers:

| Model | Input price | Output price | Cost per 1,000 calls | Notes |
|-------|-------------|--------------|----------------------|-------|
| Llama 3.1 8B | $0.05/M | $0.08/M | ~$0.07 | Fast, may miss nuance |
| Llama 3.3 70B | $0.59/M | $0.79/M | ~$0.84 | Good quality balance |
| GPT-4o | $2.50/M | $10.00/M | ~$5.50 | High quality, expensive |

For a summarisation task, Llama 3.3 70B is likely sufficient and costs 85% less than GPT-4o per call.

(Prices as of mid-2025. Always check current pricing on the provider's website.)

---

## Now go do the practical

Open `try-it-yourself.md`. You will measure real latency and token usage across different models and prompt lengths, then apply the 5 levers and see the numbers change.

---

## Going deeper (optional)

Open `deep-dive.md` for more on streaming, batching, cost monitoring in production, and how to build a model router.

---

## Congratulations

This is the final chapter of the course.

You now understand how LLMs work, how to prompt them well, how to prevent hallucinations, how to build system prompts, how to ground them in your own data with RAG and vector databases, how to evaluate them properly, how to give them tools and build agents, and how to think about cost and latency when shipping real products.

That is the full foundation. Everything else is applying these ideas to specific problems.

Keep building. Keep shipping. The gap between knowing this and being good at it closes with practice.
