# Deep dive: Cost and latency in production

Optional reading. Skip if you just want to use AI. Read if you want to understand it.

---

## Streaming

By default, the API waits until the entire reply is generated before sending anything back. For a 200-token reply at 100 tokens per second, the user waits 2 seconds staring at a blank screen.

Streaming changes this. The API sends tokens back as they are generated, one at a time. The user sees the reply appearing word by word, like ChatGPT does.

The total time to complete is the same. But the perceived latency drops dramatically because the user sees progress immediately.

In code, enabling streaming is a one-line change:

```python
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    stream=True  # enable streaming
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

For any user-facing AI feature, streaming should be the default. It makes the product feel faster even when it is not.

---

## Batching

If you are running AI in the background (not in response to a live user), batching is a major cost saver.

Instead of sending 1,000 individual API calls, you queue them and send them in batches. Most providers offer a batch API at 50% of the standard price, with a slower turnaround (minutes to hours instead of seconds).

Use cases for batching: processing historical data, running nightly evaluations, generating reports overnight, classifying a large backlog of tickets.

Do not batch anything a user is waiting for in real time.

---

## Prompt caching

When your system prompt is the same across many calls, prompt caching lets the provider process it once and reuse the result.

How it works:
1. Your first call processes the system prompt fully and caches it
2. Subsequent calls with the same system prompt prefix skip the processing step
3. You pay a reduced rate (or nothing) for the cached tokens

Savings: on a 500-token system prompt used across 100,000 calls per month, caching can save millions of tokens per month.

Availability: Anthropic (Claude), OpenAI (GPT-4o), and Groq all support caching in different forms. Check current documentation for each.

---

## Cost monitoring in production

Without monitoring, costs are invisible until the bill arrives.

Basic monitoring setup:
1. Log every API call with token counts
2. Track daily and monthly totals
3. Set alerts if daily cost exceeds a threshold
4. Tag calls by feature or user type so you know which part of the product is expensive

Tools that help: LangSmith, Helicone, and Portkey all add an observability layer on top of your LLM calls. They track costs, latency, and errors automatically.

---

## Building a model router

A model router sends simple requests to a cheap model and complex requests to an expensive model.

Simple implementation:
1. Count the input tokens or classify the complexity of the request
2. If tokens are under a threshold and the task is simple, route to Tier 1
3. Otherwise, route to Tier 2 or Tier 3

More sophisticated implementation:
- Train a small classifier to predict whether a request needs a powerful model
- Use the cheap model first and only escalate to the expensive model if confidence is low

A well-tuned router can handle 70 to 80% of traffic on cheap models, cutting costs significantly while maintaining quality on the harder requests.

---

## The total cost of ownership

API costs are only part of the picture. When estimating the real cost of an AI feature, include:

- **API costs** (what you pay per token)
- **Infrastructure** (servers, databases, vector store hosting)
- **Engineering time** (building, maintaining, evaluating)
- **Human review** (if the feature requires spot-checking outputs)
- **Failure cost** (what it costs when the model gets it wrong)

The last one is often ignored. A hallucination in a customer-facing product can cost far more than the API bill.

---

## Model selection is not permanent

Models improve constantly. A model you evaluate today may be replaced by a better, cheaper one in 6 months.

Build your system so the model is swappable. Keep your eval set. When a new model releases, run your evals on it and switch if it scores better. Do not hardcode your product to a specific model version.

This is why the eval set from Chapter 8 is one of the most valuable things you can build. It is not just a testing tool. It is the migration tool for every model upgrade.
