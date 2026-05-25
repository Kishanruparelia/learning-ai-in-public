# CLAUDE.md - Project Context for Claude Code

This file gives you (Claude Code) full context to help Kishan (Kishu) work on the **learning-ai-in-public** project. Read this fully before responding to any request in this repo.

---

## Who is the user

**Name:** Kishan Ruparelia (Kishu)
**Role:** AI Product Manager at SBI Securities
**Background:** 8 years in fintech, broking, growth, product. Strong on business and product, lighter on hands-on code (knows Next.js, PostgreSQL, TypeScript, Python at a working level, uses Cursor and now Claude Code).
**Goal of this project:** Become a top-tier AI Product Builder. Learn AI deeply by building in public, taking notes, shipping demos, then teaching others through the same artifacts.
**Learning style:** Hands-on first. Take notes, then build, then test retention. Believes the best way to learn is to teach. Wants to be treated as if learning from scratch.

---

## The learning framework

Every unit in this repo follows 4 stages, in order. We never skip a stage.

1. **Concept** — written notes in plain language. Output: `01-notes.md`
2. **Code** — hands-on demo or notebook. Output: `02-demo.py` (or similar)
3. **Application** — map concept to real SBI Securities usecases. Output: `03-application-sbi.md`
4. **Test** — self-check questions or build challenge to confirm retention. Output: `04-test.md`

Each unit lives in its own folder: `unit-XX-topic-name/`

---

## The build environment

- **OS:** macOS
- **Editor:** Claude Code (this tool) for all file edits and execution
- **Repo:** `~/learning-ai-in-public/` (local), pushed to GitHub at `github.com/Kishanruparelia/learning-ai-in-public`
- **Language:** Python 3.10+
- **LLM API for demos:** Groq (free tier, no credit card needed). Model: `llama-3.3-70b-versatile`
- **Env variable:** `GROQ_API_KEY` is already set in `~/.zshrc`
- **Packages used so far:** `groq`

---

## The SBI Securities AI roadmap (2026)

Kishu is the AI PM and is responsible for shipping usecases in this list. Every Application stage (Stage 3) must connect the unit's concept to one or more of these. Reference them often.

**Sales Force:** AI Call Quality Analyzer, AI Learning Platform, AI RM Co-Pilot
**Client Experience:** AI Customer Service Hub, AI Outbound Dealing Agent, AI Portfolio Intelligence
**Research:** AI Research Co-Pilot, AI Earnings Analyzer, AI Trading Pattern Intel
**Productivity:** AI + RPA Automation, AI Macro & Script Generator, AI Meeting Intelligence
**People & Compliance:** AI Recruiter, AI Attrition Predictor, AI Trade Surveillance
**Forecasting:** AI Sales Forecasting
**Data & Analytics:** Customer 360, Natural Language BI, Competitor Intelligence Bot
**Operations:** AI Trade Settlement Engine, AI Reconciliation Engine, eKYC Automation, Corporate Actions Bot

Each has KPIs. The full sheet is at https://docs.google.com/spreadsheets/d/1xOk3kymMV4kM73BLaJgsHT5Oo8IKYZlDUebfqlq8vWU/

---

## How you (Claude Code) should behave in this repo

1. **Treat Kishu as a learner.** Heavily comment code on first pass. Explain every non-obvious line. He has working Python knowledge but is new to AI builder patterns.
2. **No em dashes or hyphens** in any prose you write. He has explicitly asked for this. Use commas, periods, or parentheses instead.
3. **One step at a time.** Do not jump ahead. Wait for confirmation before moving to the next stage.
4. **Number-driven explanations** beat theoretical ones. If you can show, do not tell.
5. **Casual, human tone.** Not formal, not listicle-heavy. Conversational.
6. **If he asks to fix his own writing, only fix spelling and grammar.** Do not rewrite his content.
7. **Run code when asked, paste output back.** He wants to see real outputs, not hypotheticals.
8. **Commit after each stage** with a clear message like `unit-01: stage 2 complete (code demo working)`.

---

## Current unit in progress

**Unit 1: Hallucinations**

Stage 1 (Concept) — DONE. File: `unit-01-hallucinations/01-notes.md`
Stage 2 (Code) — IN PROGRESS. File to build: `unit-01-hallucinations/02-demo.py`
Stage 3 (Application) — PENDING
Stage 4 (Test) — PENDING

---

## Unit 1, Stage 2 build instructions

Build the file `unit-01-hallucinations/02-demo.py` exactly as specified below.

### Purpose
Make Llama 3.3 70B (via Groq) hallucinate on purpose, one type at a time, so Kishu can see each failure live. Then show the fix for each type. 5 experiments, top to bottom, runnable as a story.

### Requirements
1. Heavily commented for a learner.
2. Uses the `groq` Python SDK.
3. Reads `GROQ_API_KEY` from environment.
4. Has a small helper function `ask_llm(prompt, system="")` so we do not repeat ourselves.
5. Each experiment has a clear banner, the prompt, the broken response, then the fix prompt and the fixed response.
6. For Experiment 3 (Instruction), check programmatically whether the response contained the forbidden word "opportunity" and print the verdict.

### The 5 experiments to include

**Experiment 1: Factual Hallucination**
- Trigger: Ask for the exact closing price of Reliance Industries on NSE on 14th August 2023.
- Fix: Add "If you do not have this data with certainty, say so explicitly instead of guessing."

**Experiment 2: Fabrication**
- Trigger: Ask for the exact SEBI circular number governing MTF eligibility for retail investors, with circular number, date, and section.
- Fix: Tell it not to fabricate, to say so if unsure, and to suggest where to search instead.

**Experiment 3: Instruction Hallucination**
- Trigger: A dense prompt about an IPO client message that buries the rule "do not use the word opportunity" in the middle.
- Fix: Move the rule to a system prompt as a CRITICAL RULE.
- Print whether "opportunity" appeared in each version's response.

**Experiment 4: Context Hallucination**
- Trigger: Provide a portfolio note saying Mr. Sharma has 80% commodities, 15% equity, 5% FD. Ask for a 2-line summary. See if the model changes the unusual percentages.
- Fix: Add explicit grounding rules: "Use ONLY the information provided below. Do not add information from your general knowledge. Quote the exact percentages."

**Experiment 5: Logical Hallucination**
- Trigger: A multi-step math question about a 2-stock portfolio. Rs 5,00,000 in Stock A (up 12%) and Rs 3,00,000 in Stock B (down 8%) over 6 months. Ask for total profit/loss in Rs and percentage return. Ask for "just the final numbers" (no reasoning).
- Show the correct answer: Stock A profit Rs 60,000, Stock B loss Rs 24,000, net profit Rs 36,000, total invested Rs 8,00,000, portfolio return 4.5%.
- Fix: Force step-by-step reasoning (chain of thought) by listing the steps the model should take.

### After building
1. Run it with `python 02-demo.py`.
2. Save the full output to `02-demo-output.txt`.
3. Show me (Kishu) the output so we can review it together in the Claude.ai chat.

---

## What happens after Stage 2

Once Stage 2 is done and output looks clean, Kishu will paste the output back into his Claude.ai chat. There, his learning Claude will lead him through Stage 3 (Application to SBI usecases) and Stage 4 (Test). Once both are done, he comes back here to commit the new files and start Unit 2.

---

## Notes for future units (do not act on these now)

Planned unit order, subject to change based on Kishu's needs at SBI:

- Unit 2: Prompt Engineering (the real craft, not the hype)
- Unit 3: System Prompts and Role Design
- Unit 4: Structured Outputs (JSON, function calling)
- Unit 5: RAG fundamentals (Retrieval Augmented Generation)
- Unit 6: Vector Databases
- Unit 7: Evaluations (how to test AI products)
- Unit 8: Agents and Tool Use
- Unit 9: Cost, latency, and model selection
- Unit 10: Going to production (logging, monitoring, fallbacks)

---

## The /course folder

A separate non-technical, hour-paced course track lives at `/course/`. It is written for complete beginners (no coding background). Each lesson has 4 files: README, try-it-yourself, deep-dive (optional), test.

### Course progress

**Lesson 1: What is an LLM** — DONE. Files live at `course/lesson-01-what-is-an-llm/`.
- Step 2 updated twice: replaced Homebrew with python.org .pkg installer after Homebrew caused install failures.
- Reader is currently on Practical 3, Step 2 (installing Python via python.org).

**Lesson 2: Tokens** — PENDING. Tiktokenizer link goes in the practical section.

---

End of context file.
