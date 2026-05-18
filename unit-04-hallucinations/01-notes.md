# Unit 1: Hallucinations

## What is a hallucination?

A hallucination is when an AI confidently states something that is not true.

The dangerous word is "confidently". A human who doesn't know says "I'm not sure". An LLM by default gives wrong answers in the same tone as correct ones. That tone problem is what makes hallucination a product issue, not just a research curiosity.

## Why do LLMs hallucinate? (the one mental model)

An LLM is not a database. It is not a search engine. It does not look things up.

What it actually does: given the words so far, predict the most likely next word. Then the next. Every output is a prediction of plausible-sounding text based on patterns from training.

So when you ask "What was Reliance Q2 FY24 revenue?", the model does not fetch a number. It generates a sequence of words that sound like a financial answer. Sometimes the words are correct because the pattern was seen enough during training. Sometimes they are slightly off. Sometimes they are completely invented but phrased perfectly.

**The key insight: hallucination is not a bug. It is the same mechanism that produces all output. Correct answers and hallucinations come from the exact same process. The model has no internal signal that says "I know this" vs "I am guessing".**

## The 5 types of hallucinations

Memory hook: **FFCIL** (Find Fakes In Claude's Logic)
Or remember: AI can lie about **what** (Factual, Fabrication), **how** (Instruction, Context), or **why** (Logical).

### Family A: Hallucinations about facts (what is true)

**1. Factual** — right shape, wrong value. The thing exists, the number/detail is wrong.
- Example: "TCS Q2 FY26 revenue was Rs 64,000 cr" when actual was Rs 65,200 cr.

**2. Fabrication** — the thing itself does not exist. Invented from thin air.
- Example: "As per SEBI Circular CIR/MIRSD/19/2025" when no such circular was issued.

### Family B: Hallucinations about the task (what was asked)

**3. Instruction** — ignored HOW you asked. Format, tone, length, or rules.
- Example: Asked for 3 lines, got 10. Asked for polite, got harsh.

**4. Context** — ignored WHAT you gave it. Contradicts your pasted document or prior message.
- Example: You paste a portfolio showing 60% equity, AI summary says 40% equity.

**5. Logical** — facts are right, reasoning is wrong.
- Example: "Stock X is down 2%, Stock Y is up 1%, therefore Y outperformed X by 3x".

## Why this matters for SBI Securities 2026 roadmap

Each type maps to a different fix. This is what an AI PM gets paid to know.

| Type | Fix |
|------|-----|
| Factual | RAG (give it the right data at query time) |
| Fabrication | Grounding + citation requirements |
| Instruction | Better prompting (clear system prompts, examples) |
| Context | Prompt design + system prompt structure |
| Logical | Reasoning techniques (chain of thought, tool use, calculators) |

If you call everything "fabrication" you cannot choose the right solution.

### Direct hits in the SBI usecase list

- **AI Research Co-Pilot** has KPI "factual accuracy >= 99%". Targets Factual + Fabrication.
- **AI Customer Service Hub** has containment rate target 70%. Every Instruction hallucination drops it.
- **Natural Language BI** lets users ask questions in English and get data. Logical hallucinations here mean wrong numbers in the CEO's dashboard. Highest stakes.
- **AI Earnings Analyzer** has "beat/miss directional accuracy >= 90%". Logical hallucinations break this.
- **AI Portfolio Intelligence** sends alerts. A Factual or Logical hallucination here goes to clients directly.

## Quick self-check questions (to revisit before interviews)

1. Why is hallucination not a bug?
2. What is the difference between Factual and Fabrication?
3. What is the difference between Instruction and Context?
4. Which type does RAG fix? Which type does chain-of-thought fix?
5. Why do we differentiate the 5 types instead of calling all of it "hallucination"?
