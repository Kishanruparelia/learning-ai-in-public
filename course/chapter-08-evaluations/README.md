# Chapter 8: Evaluations

**Time needed:** 1 hour
**You will need:** A browser, your Groq API key, Google Colab open

---

## What you will be able to do by the end

1. Explain why evaluations are the difference between a demo and a product
2. Write a basic eval set for any AI task
3. Run automated evaluations using an LLM as a judge
4. Know which eval method to use for different types of AI tasks

---

## The big idea

Anyone can build an AI demo that works on 3 examples.

A product has to work on 3,000 examples, including the weird ones, the edge cases, and the inputs you did not think of.

Evaluations are how you measure that. They are tests for AI. Without them, you are flying blind. You change a prompt, you do not know if it got better or worse. You switch models, you have no idea which one to trust. You ship, and the first complaint from a real user is your feedback loop.

Evals give you a number. A score. Something you can track, compare, and improve.

---

## Why evals are skipped and why that is a mistake

Evals feel like extra work when you are trying to ship fast.

But without evals, every change you make to a prompt, a model, or a retrieval system is a guess. You might improve one thing and break three others without realising it.

In software, this is what automated tests solve. In AI, evals solve the same problem. They are the test suite for your AI system.

---

## The 4 types of AI tasks and how to evaluate each

### Type 1: Exact answer tasks
The correct answer is fixed and unambiguous.

Examples: classification, data extraction, yes/no questions.

How to evaluate: string match or exact comparison.

```
Question: "Is this email a complaint or a query?"
Correct answer: "Complaint"
Model answer: "Complaint"
Result: Pass
```

Score = number of correct answers / total questions.

---

### Type 2: Structured output tasks
The model must return data in a specific format (JSON, table, list).

Examples: extracting fields from a document, generating a report with specific sections.

How to evaluate: check that the output parses correctly, then check individual fields.

```
Expected: {"category": "billing", "urgency": "high"}
Model output: {"category": "billing", "urgency": "high"}
Result: Pass on both fields
```

---

### Type 3: Open-ended text tasks
The correct answer is not fixed. A good summary, a well-written email, a helpful explanation.

How to evaluate: use an LLM as a judge. You describe what "good" looks like and ask a second LLM to score the output.

This is called LLM-as-a-judge and it is now standard practice in AI evaluation.

---

### Type 4: RAG tasks
The model must retrieve the right document and then answer correctly from it.

Two things can go wrong independently:
1. The wrong document was retrieved (retrieval failure)
2. The right document was retrieved but the answer was wrong (generation failure)

Evaluate both separately so you know where the problem is.

---

## LLM-as-a-judge: the most useful eval technique

For open-ended tasks, you cannot do exact matching. But you can ask a second LLM to evaluate the output.

Here is how it works:

```
You are an evaluator. A user asked the following question:
[QUESTION]

The AI gave the following answer:
[AI ANSWER]

Score the answer from 1 to 5 on each of these dimensions:
- Accuracy: is the information correct?
- Helpfulness: does it actually answer what was asked?
- Conciseness: is it appropriately brief without missing key information?

Return your scores as JSON: {"accuracy": X, "helpfulness": X, "conciseness": X}
```

You run this for every example in your eval set. Average the scores. Now you have a number.

Change your prompt. Run evals again. Did the number go up or down? Now you know.

---

## Building an eval set

An eval set is a collection of test cases. Each test case has:
- An input (the user's question or message)
- An expected output or criteria for a good output

How many do you need? Start with 20 to 50 examples for a new task. Cover:
- Typical cases (the most common inputs you expect)
- Edge cases (unusual inputs, short inputs, very long inputs)
- Failure cases (inputs where you know the model tends to go wrong)

Where do you get them? From real user data (anonymised), from domain experts who can write realistic examples, or by generating them with an LLM and then reviewing them manually.

---

## The eval loop

This is the workflow every serious AI team follows:

1. Build the eval set before you build the product
2. Run evals on the first version. Get a baseline score.
3. Make a change (prompt, model, retrieval, chunking)
4. Run evals again. Did the score improve?
5. Keep only changes that improve the score
6. Add new test cases when you find new failure modes

This loop is what separates teams that ship reliable AI from teams that ship demos that embarrass them in front of users.

---

## Now go do the practical

Open `try-it-yourself.md`. You will build an eval set, run LLM-as-a-judge scoring, and then change a prompt and see the score change.

---

## Going deeper (optional)

Open `deep-dive.md` for more on eval frameworks, human vs LLM evaluation trade-offs, and how to handle model-graded evals at scale.

---

## Check yourself

Open `test.md` before moving to Chapter 9.
