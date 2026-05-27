# Deep dive: Agents in production

Optional reading. Skip if you just want to use AI. Read if you want to understand it.

---

## Why agents fail in production

Agents work beautifully on demos. They break in production for predictable reasons.

**Compounding errors:** Each step introduces a small chance of error. Over a 5-step agent, even a 90% accuracy per step gives you 0.9^5 = 59% chance of completing correctly. A 10-step agent at 90% per step is only 35% likely to complete without error.

**Hallucinated tool calls:** The model might call a tool with incorrect arguments, or call a tool that does not exist, because it predicted that a tool call looked right in context.

**Infinite loops:** Without a step limit, an agent can get stuck in a loop, calling the same tool repeatedly.

**Irreversible actions:** An agent that sends emails, writes to a database, or makes API calls can cause real-world damage before a human notices.

Mitigation strategies:
- Always set a maximum number of steps
- Log every tool call so you can audit what happened
- For high-risk actions (write, delete, send), require human confirmation before executing
- Build a dry-run mode that simulates tool calls without executing them

---

## Memory in agents

The basic agent in this chapter has no memory between conversations. Each new session starts fresh.

For agents that need to remember things across sessions, there are three approaches:

**In-context memory:** Summarise previous conversations and inject the summary into the system prompt. Simple but token-heavy.

**External memory:** Store important facts in a database. At the start of each session, retrieve relevant facts and inject them. Scales better than in-context.

**Episodic memory:** Store entire past interactions as searchable documents in a vector database. Retrieve relevant past episodes when needed. Most powerful but most complex.

---

## Multi-agent systems

A single agent handles one task. A multi-agent system has multiple specialised agents that hand off to each other.

Example: a research agent finds and summarises documents, then hands the summary to a writer agent that formats it into a report, then hands the report to a reviewer agent that checks for errors.

Each agent is smaller, more focused, and easier to evaluate than one giant agent trying to do everything.

Multi-agent systems are increasingly common in production AI but are harder to debug because failures can happen at any handoff point.

---

## Agent frameworks

Building the agent loop manually (as you did in the practical) is educational but repetitive for production work.

Popular frameworks abstract the loop:

**LangChain:** Large ecosystem, many integrations, can be complex for simple use cases.

**LlamaIndex:** Focused on RAG and document-heavy agents, clean abstractions.

**CrewAI:** Designed specifically for multi-agent collaboration.

**Autogen (Microsoft):** Good for multi-agent conversations and code execution.

These frameworks are useful, but understanding the raw mechanics first (as you now do) means you are not dependent on a framework to debug when something goes wrong.

---

## Function calling vs ReAct

There are two main ways to implement tool use:

**Function calling (what you built):** The model is given a structured list of tools and returns a structured JSON response when it wants to call one. The API handles the format. Reliable and easy to parse.

**ReAct prompting:** The model is prompted to output Thought / Action / Observation in plain text. Your code parses the text to find the action. More flexible, works with any model, but requires careful parsing.

Function calling is now supported natively by most major LLM APIs (Groq, OpenAI, Anthropic). It is the preferred approach for production systems.

---

## When to use agents vs simpler approaches

Before building an agent, ask:

1. Can this be done with a single prompt? If yes, use a single prompt.
2. Can this be done with 2 or 3 fixed steps in sequence? If yes, use a pipeline (not an agent).
3. Does the next step genuinely depend on the result of the previous step in a way you cannot predict in advance? If yes, an agent might be appropriate.

Agents add complexity, cost, and failure modes. They are the right tool when the task genuinely requires adaptive multi-step reasoning. They are the wrong tool when a simpler approach would work.
