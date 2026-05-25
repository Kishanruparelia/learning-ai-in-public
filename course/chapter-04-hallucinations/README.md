# Chapter 4: Hallucinations

**Time needed:** 1 hour
**You will need:** A browser, your Groq API key, Google Colab open

---

## What you will be able to do by the end

1. Explain what a hallucination is and why it happens
2. Recognise the 5 types of hallucination
3. Write prompts that reduce hallucinations significantly
4. Know which AI tasks are high-risk vs low-risk for hallucinations

---

## The big idea

An LLM does not know the difference between something it is certain about and something it is guessing.

It generates the next most likely token either way. It sounds equally confident when it is right and when it is completely making things up.

This is not a bug that will be fixed. It is a fundamental property of how prediction engines work. The skill is learning when to trust the output, when to verify it, and how to prompt in ways that reduce the risk.

---

## What is a hallucination

A hallucination is when an AI generates output that is confident, fluent, and wrong.

Not "I don't know". Not a vague hedge. A specific, detailed, convincingly written answer that is factually incorrect or entirely fabricated.

Real examples from financial contexts:

- Asked for a SEBI circular number: the model gives a plausible-sounding circular number that does not exist.
- Asked for a stock's closing price on a specific date: the model gives a number that was never the actual price.
- Asked to summarise a document: the model adds facts that were not in the document.

All of these are hallucinations. All sound completely credible.

---

## The 5 types of hallucination

### Type 1: Factual hallucination
The model states something false as if it is true.

> "Reliance Industries closed at Rs 2,487 on 14th August 2023."

The model has no real-time data access. It guessed a number that sounded plausible for Reliance at that time.

**Why it happens:** The model learned to produce confident factual statements. It never learned to say "I don't have this data."

---

### Type 2: Fabrication
The model invents specific details that do not exist.

> "SEBI Circular SEBI/HO/MRD/DP/CIR/2022/0089 dated 14 March 2022, Section 4.3..."

That circular may not exist at all. The model constructed a plausible-looking reference because it has seen thousands of real SEBI circular citations.

**Why it happens:** The model is pattern-matching. SEBI circulars follow a format. It filled in the format convincingly.

---

### Type 3: Instruction hallucination
The model ignores or forgets part of your instructions, usually when the prompt is long or complex.

You say: "Do not use the word opportunity."
The model uses "opportunity" anyway.

**Why it happens:** The model is predicting the most likely response to your message. Buried constraints in a long prompt get less weight than the primary task.

**Fix:** Put critical rules in the system prompt, not buried in the middle of a long user message.

---

### Type 4: Context hallucination
The model adds information that was not in the source material you provided.

You paste a client's portfolio note: "Mr. Sharma holds 80% commodities, 15% equity, 5% FD."
You ask for a summary.
The model writes: "Mr. Sharma has a diversified portfolio with a balanced allocation..."

The model smoothed over an unusual allocation because it contradicted what a "normal" portfolio looks like. It hallucinated normalcy.

**Why it happens:** The model's training taught it what things usually look like. When your data is unusual, it corrects toward the usual.

**Fix:** Explicitly tell the model to use only the provided information and quote exact figures.

---

### Type 5: Logical hallucination
The model makes a reasoning error, usually in multi-step calculations or inferences.

You ask: "Stock A is up 12%, Stock B is down 8%. What is the average return?"
The model says: "2%."

That is wrong. The average of +12 and -8 is +2, not 2 in the sense the model might present it, but the model might also skip a step and give a different wrong number entirely.

**Why it happens:** Each token is generated based on what came before. Without being forced to show working, the model jumps to an answer that "looks right" without actually computing it.

**Fix:** Chain of thought. Force the steps.

---

## The risk spectrum

Not all AI tasks carry the same hallucination risk. Here is how to think about it:

**High risk (always verify):**
- Specific dates, prices, numbers
- Legal or regulatory references (SEBI circulars, RBI guidelines)
- Medical or compliance advice
- Anything where being wrong has real consequences

**Medium risk (spot-check):**
- Summaries of documents you provided
- Classification tasks
- Drafting emails or messages

**Low risk (generally safe):**
- Reformatting existing content
- Translation between styles or tones
- Brainstorming ideas (wrong ideas are fine, you are just generating options)
- Explaining concepts in simple language

The key question before using AI output: "What happens if this is wrong?"

---

## The 4 fixes

| Hallucination type | Fix |
|-------------------|-----|
| Factual | Tell it to say "I don't know" if uncertain. Do not ask for data it cannot have. |
| Fabrication | Ask it to say "I cannot find this" instead of inventing. Tell it where to look instead. |
| Instruction | Move critical rules to a system prompt. Keep user prompts short. |
| Context | Ground it explicitly: "Use ONLY the information below. Quote exact figures." |
| Logical | Chain of thought. List every step it must take before the final answer. |

---

## Now go do the practical

Open `try-it-yourself.md`. You will trigger each type of hallucination deliberately, then apply the fix and compare the outputs.

---

## Going deeper (optional)

Open `deep-dive.md` for the technical reason hallucinations are impossible to eliminate entirely, and what RAG does to reduce them.

---

## Check yourself

Open `test.md` before moving to Chapter 5.
