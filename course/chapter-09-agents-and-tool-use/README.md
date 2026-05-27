# Chapter 9: Agents and Tool Use

**Time needed:** 1 hour
**You will need:** A browser, your Groq API key, Google Colab open

---

## What you will be able to do by the end

1. Explain what an AI agent is and how it differs from a chatbot
2. Understand what tool use means and why it extends what an LLM can do
3. Build a simple agent that uses tools to answer questions it could not answer alone
4. Know the risks of agents and when not to use them

---

## The big idea

Every AI system you have built so far takes one input and produces one output.

You send a message. The model replies. Done.

An agent is different. It takes a goal and figures out the steps needed to reach it. Along the way it can use tools, make decisions, run multiple steps, and adjust based on what it finds.

A chatbot answers questions. An agent gets things done.

---

## What is an agent

An agent is an LLM that has been given the ability to take actions, not just generate text.

Those actions are called tools. A tool is any function the model can choose to call.

Examples of tools:
- Search the web
- Run a calculation
- Look up a database record
- Send an email
- Read a file
- Call an API

The model decides which tool to use, calls it, gets the result, and then decides what to do next. It keeps going until it reaches the goal or runs out of steps.

---

## How tool use works

The key insight is that the LLM does not actually run the tool. It decides to use it.

Here is the flow:

1. You tell the model what tools are available (their names and what they do)
2. The model looks at the user's request and decides which tool to call
3. The model outputs a structured request: "call this tool with these inputs"
4. Your code intercepts that request, actually runs the tool, and gets the result
5. The result is fed back to the model
6. The model uses the result to continue reasoning or produce a final answer

The LLM is the brain. Your code is the hands.

---

## A simple example

User asks: "What is 20% of 847, and is that number even or odd?"

Without tools, the model might guess or calculate wrong.

With a calculator tool:

1. Model sees the question
2. Model decides to call `calculate("847 * 0.20")`
3. Your code runs the calculation: result is 169.4
4. Model receives 169.4
5. Model answers: "20% of 847 is 169.4. Since 169.4 is not a whole number, the even/odd question does not apply."

The model contributed the reasoning and the decision. The tool contributed the accurate number.

---

## The ReAct pattern

The most common agent design is called ReAct, which stands for Reason + Act.

The model alternates between two types of output:

**Thought:** The model reasons about what to do next.
**Action:** The model calls a tool.

After getting the tool result, it reasons again, then acts again, until it has enough to answer.

Example for "What is the population of the 3 largest cities in Australia?":

```
Thought: I need to find the 3 largest cities in Australia first.
Action: search("largest cities in Australia by population")
Result: Sydney, Melbourne, Brisbane

Thought: Now I need the population of each city.
Action: search("Sydney population 2024")
Result: approximately 5.3 million

Action: search("Melbourne population 2024")
Result: approximately 5.1 million

Action: search("Brisbane population 2024")
Result: approximately 2.6 million

Thought: I have all the data I need.
Final answer: Sydney (5.3M), Melbourne (5.1M), Brisbane (2.6M)
```

Each step is small. The model is not trying to do everything at once.

---

## What agents are good at

| Use case | Why agents help |
|----------|----------------|
| Multi-step research tasks | Need to search, find, then reason across results |
| Tasks that require real-time data | Tools can fetch live data the model does not have |
| Tasks with conditional logic | Next step depends on what previous step returned |
| Automating workflows | Sequence of actions across multiple systems |

---

## What agents are bad at

| Problem | Why it matters |
|---------|---------------|
| Unpredictable paths | Hard to test every possible sequence of steps |
| Compounding errors | A wrong decision early causes cascading failures |
| Long chains are expensive | Every tool call costs tokens and time |
| Hard to debug | When it fails, finding which step went wrong takes effort |
| Real-world actions are hard to undo | An agent that sends an email or deletes a record cannot take it back |

The rule of thumb: use an agent when the task genuinely requires multiple steps where each step depends on the result of the previous one. Do not use an agent just because it sounds impressive.

---

## Now go do the practical

Open `try-it-yourself.md`. You will build an agent with 3 tools: a calculator, a unit converter, and a data lookup function. Give it multi-step questions and watch it reason through them.

---

## Going deeper (optional)

Open `deep-dive.md` for more on multi-agent systems, memory in agents, and how production agent frameworks like LangChain and LlamaIndex handle this.

---

## Check yourself

Open `test.md` before moving to Chapter 10.
