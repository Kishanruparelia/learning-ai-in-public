# Chapter 9 Test

Answer in your own words. No looking back. Answers at the bottom. Do not scroll until you are done.

---

## Question 1
In the tool use flow you built, the LLM does not actually run the tool. What does it do, and what runs the tool instead?

## Question 2
An agent has 8 steps. Each step has a 92% chance of being correct. What is the approximate probability that the entire task completes without a single error? What does this tell you about designing agents?

## Question 3
Your manager asks you to build an AI agent that automatically sends follow-up emails to leads after a sales call. What is the one biggest risk you would flag before building this, and how would you mitigate it?

---
---
---
---
---

## Answers (no peeking)

**Q1:** The LLM decides which tool to call and outputs a structured request describing the tool name and the arguments. Your code intercepts that request and runs the actual function. The result is then fed back to the LLM. The LLM is the decision maker. Your code is the executor.

**Q2:** 0.92^8 = approximately 51%. Roughly a coin flip. This tells you that even highly reliable individual steps compound into unreliable end-to-end outcomes over long chains. Agents should be kept as short as possible, each step should be as reliable as possible, and there should always be a fallback or human review step for long chains.

**Q3:** The biggest risk is irreversibility. Once an email is sent, it cannot be unsent. If the agent misreads the context, sends at the wrong time, or sends to the wrong person, the damage is immediate and visible to the customer. Mitigation: start with a human-in-the-loop mode where the agent drafts the email and queues it for a human to approve before sending. Only automate the send step after you have evaluated the drafts over hundreds of real examples and are confident in the quality.

---

If you got all three right, move to Chapter 10: Cost, Latency, and Model Selection.

If Q2 surprised you, work through the maths on your own for a 5-step and 10-step agent at various accuracy levels. The numbers are humbling and directly inform how you should design production agents.
