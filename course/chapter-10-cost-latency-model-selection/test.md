# Chapter 10 Test

Answer in your own words. No looking back. Answers at the bottom. Do not scroll until you are done.

---

## Question 1
Name the 5 levers for reducing cost and latency. One sentence each.

## Question 2
Your AI feature costs $0.0004 per call. The product manager says it will get 500,000 calls per month at launch. What is the monthly API cost, and what is one lever you would check first to reduce it?

## Question 3
A colleague argues: "We should always use the most powerful model to make sure quality is high." What is wrong with this reasoning, and what would you do instead?

---
---
---
---
---

## Answers (no peeking)

**Q1:**
1. **Shorter system prompts:** Cut unnecessary words from your system prompt since it is charged on every single call.
2. **Limit output length:** Tell the model explicitly how short to be, cutting output tokens and latency directly.
3. **Cache repeated inputs:** Use prompt caching so a fixed system prompt is not reprocessed on every call.
4. **Use a smaller model for simple tasks:** Route low-complexity requests to a cheap fast model and reserve large models for hard tasks.
5. **Reduce conversation history:** Summarise or trim old turns instead of passing the full history every time.

**Q2:** 500,000 × $0.0004 = $200 per month. The first lever to check is output length. Output tokens cost 2x to 3x more than input tokens and directly drive latency. If replies are currently 200 words and could reasonably be 50 words, that alone cuts output cost by 75%.

**Q3:** The most powerful model is not always the right model. It costs 10x to 100x more than smaller models, is slower, and for simple tasks like classification or short-form generation, a smaller model performs equally well. The right approach is to define your quality threshold using an eval set, test candidate models against it, and use the smallest model that meets the threshold. Paying for capability you do not need is waste.

---

You have finished the course.

You now have the foundation to build real AI products. Not just demos. Products with proper prompting, grounded in data, tested with evaluations, with guardrails that hold, and costs you can actually defend in a budget meeting.

The next step is yours. Pick something. Build it.
