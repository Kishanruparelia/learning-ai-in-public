"""
Unit 1: Hallucinations, Stage 2 (Code Demo)
============================================
Goal: Make Llama 3.3 70B hallucinate on purpose, one type at a time,
so you can see each failure live. Then show the fix for each type.

Run with:
    python 02-demo.py

You need:
    GROQ_API_KEY set in your environment (already done via ~/.zshrc)
    pip install groq
"""

# We import the Groq SDK. This is a Python library that lets us talk
# to the Groq API, which hosts Llama 3.3 70B for free.
from groq import Groq

# Groq() with no arguments automatically reads your GROQ_API_KEY
# from the environment. You never paste the key in code. This is
# the standard safe pattern for all API clients.
client = Groq()

# This is the model we use throughout the demo. Llama 3.3 70B is
# Groq's strongest free model. It hallucinates more than GPT-4 or
# Claude, which is actually useful for this learning exercise.
MODEL = "llama-3.3-70b-versatile"


# ---------------------------------------------------------------
# Helper function: ask_llm
# ---------------------------------------------------------------
# We define a small reusable function so we do not write the same
# 10 lines of Groq API code five times. This is called DRY (Do not
# Repeat Yourself), a basic coding principle.
#
# Parameters:
#   prompt  (str) : The user message we send to the model.
#   system  (str) : An optional system prompt. System prompts tell
#                   the model how to behave before the user speaks.
#                   If we leave this blank, we use a generic default.
#
# Returns:
#   str : The model's reply as a plain string.
# ---------------------------------------------------------------
def ask_llm(prompt: str, system: str = "") -> str:

    # messages is a list of turns in the conversation.
    # The Groq API (like OpenAI's) uses the format:
    #   [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
    # The system role sets the rules. The user role is the actual question.
    messages = []

    if system:
        # If a system prompt was provided, add it as the first message.
        messages.append({"role": "system", "content": system})
    else:
        # If no system prompt was given, use a neutral default.
        # This keeps the model from adding extra disclaimers on its own.
        messages.append({"role": "system", "content": "You are a helpful assistant."})

    # Add the actual user question after the system message.
    messages.append({"role": "user", "content": prompt})

    # Send the messages to the Groq API.
    # max_tokens=500 limits how long the reply can be.
    # We do not need essays, just enough to see the hallucination.
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=500,
        messages=messages,
    )

    # The API returns a response object. The actual text lives here:
    # response.choices[0].message.content
    # choices[0] means the first (and only) reply.
    # message.content is the string text of that reply.
    return response.choices[0].message.content


# ---------------------------------------------------------------
# Helper function: banner
# ---------------------------------------------------------------
# Just prints a visible separator line so the output is easy to
# read when you scroll through it top to bottom.
# ---------------------------------------------------------------
def banner(title: str):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


# ===============================================================
# EXPERIMENT 1: FACTUAL HALLUCINATION
# ===============================================================
# Definition:
#   Right shape, wrong value. The thing exists (Reliance Industries
#   does trade on NSE), but the specific number is invented.
#
# Why models do this:
#   They are trained to produce fluent, helpful answers. When they
#   do not have exact data, they fill in a plausible-looking number
#   rather than admitting uncertainty. It feels helpful. It is not.
#
# Why this matters at SBI:
#   If an AI RM Co-Pilot or Portfolio Intelligence tool gives a
#   client a wrong stock price or NAV, that is a compliance and
#   trust disaster.
# ===============================================================

banner("EXPERIMENT 1: FACTUAL HALLUCINATION")

# This prompt asks for a very specific number (a stock price on a
# specific date). The model almost certainly does not have this
# memorized. Watch what it does.
prompt_factual = (
    "What was the exact closing price of Reliance Industries on "
    "the NSE on 14th August 2023? Give me a precise number."
)

print(f"\nPROMPT:\n{prompt_factual}\n")
print("MODEL RESPONSE (likely hallucinated):")
print(ask_llm(prompt_factual))

# Now we add one simple sentence: permission to say "I don't know".
# This is the single highest return on investment prompt change
# you can make for factual accuracy.
print("\n--- THE FIX: give the model permission to say it does not know ---\n")

prompt_factual_fixed = (
    "What was the exact closing price of Reliance Industries on "
    "the NSE on 14th August 2023? Give me a precise number. "
    "If you do not have this data with certainty, say so explicitly "
    "instead of guessing."
)

print(f"PROMPT:\n{prompt_factual_fixed}\n")
print("MODEL RESPONSE (should admit uncertainty now):")
print(ask_llm(prompt_factual_fixed))


# ===============================================================
# EXPERIMENT 2: FABRICATION
# ===============================================================
# Definition:
#   The thing itself does not exist. Not a wrong number for a real
#   thing. A completely made-up thing, with perfect formatting.
#
# Why models do this:
#   They have seen thousands of SEBI circulars, legal documents, and
#   regulatory references in training. They know exactly what a
#   circular number looks like (SEBI/CIR/...). So they produce one
#   that looks completely real. There is no asterisk. No caveat.
#
# Why this matters at SBI:
#   The AI Trade Surveillance or Compliance tools could cite a fake
#   SEBI circular. A junior analyst pastes it into a report. Nobody
#   checks. That is a regulatory risk.
# ===============================================================

banner("EXPERIMENT 2: FABRICATION")

# We ask for a specific regulatory citation. The model will produce
# something that looks real and authoritative. It is not.
prompt_fabrication = (
    "Cite the exact SEBI circular number that governs margin "
    "trading facility (MTF) eligibility criteria for retail "
    "investors. Give me the circular number, date, and section."
)

print(f"\nPROMPT:\n{prompt_fabrication}\n")
print("MODEL RESPONSE (likely a fabricated circular):")
print(ask_llm(prompt_fabrication))

# The fix is to explicitly tell the model it is allowed to refuse.
# When you forbid fabrication and give it an escape hatch, it uses it.
print("\n--- THE FIX: forbid fabrication, give it an escape hatch ---\n")

prompt_fabrication_fixed = (
    "I need to cite SEBI guidelines on MTF eligibility. "
    "Only respond with information you are highly confident is real. "
    "Do not fabricate circular numbers. If you cannot recall the "
    "exact circular, say so and suggest where I should search instead."
)

print(f"PROMPT:\n{prompt_fabrication_fixed}\n")
print("MODEL RESPONSE (should refuse to fabricate now):")
print(ask_llm(prompt_fabrication_fixed))


# ===============================================================
# EXPERIMENT 3: INSTRUCTION HALLUCINATION
# ===============================================================
# Definition:
#   Model ignores HOW you asked. The facts may be fine, but it
#   broke a specific rule you gave it (format, tone, forbidden words).
#
# Why models do this:
#   When a prompt is dense, the model weighs all parts of it and
#   sometimes drops a rule buried in the middle. It prioritizes
#   producing a good-sounding response over following every constraint.
#
# Why this matters at SBI:
#   Client communication templates at SBI Securities have compliance
#   rules. Certain words may be legally restricted ("guaranteed",
#   "assured", "risk-free"). If an AI drafts a message that ignores
#   those rules, it is a SEBI violation.
#
# Setup for this experiment:
#   We bury the rule ("do not use the word opportunity") in the
#   middle of a dense prompt and see if the model catches it.
#   Then we move the rule to the system prompt where it has more
#   weight, and test again.
# ===============================================================

banner("EXPERIMENT 3: INSTRUCTION HALLUCINATION")

# The forbidden word is "opportunity". It is buried in the middle
# of a realistic, busy prompt. Watch for it in the response.
prompt_instruction = (
    "I am a relationship manager at SBI Securities. Write me a "
    "client message about the upcoming IPO of XYZ Ltd. Do not use "
    "the word 'opportunity' anywhere in the message. The client is "
    "a HNI with 5 crore portfolio, conservative risk profile, mostly "
    "in mutual funds. The IPO opens Monday. Keep it short, friendly, "
    "and professional. Mention the price band of Rs 450-475."
)

print(f"\nPROMPT:\n{prompt_instruction}\n")
print("MODEL RESPONSE (watch for the word 'opportunity'):")
response_3 = ask_llm(prompt_instruction)
print(response_3)

# We check programmatically (not by eyeballing) whether the forbidden
# word appeared. .lower() handles any capitalisation variation.
word_found = "opportunity" in response_3.lower()
print(f"\nVERDICT: Did the response contain 'opportunity'? "
      f"{'YES, RULE BROKEN' if word_found else 'No, rule followed this time'}")

# The fix is to move the critical rule out of the user prompt and into
# a system prompt. The model treats system prompts as standing orders.
# User prompts are more like requests. Rules belong in system prompts.
print("\n--- THE FIX: move the rule to the system prompt ---\n")

system_fixed = (
    "You are a client communication assistant for SBI Securities. "
    "CRITICAL RULE: You must never use the word 'opportunity' in any "
    "output under any circumstances. This is a hard compliance rule."
)

# The user prompt is now clean and short. The rule lives in the system.
prompt_instruction_fixed = (
    "Write a short client message about the upcoming IPO of XYZ Ltd "
    "for a HNI client with conservative risk profile. Price band "
    "Rs 450-475. Opens Monday."
)

print(f"SYSTEM PROMPT:\n{system_fixed}\n")
print(f"USER PROMPT:\n{prompt_instruction_fixed}\n")
print("MODEL RESPONSE:")
response_3_fixed = ask_llm(prompt_instruction_fixed, system=system_fixed)
print(response_3_fixed)

word_found_fixed = "opportunity" in response_3_fixed.lower()
print(f"\nVERDICT: Did the response contain 'opportunity'? "
      f"{'YES, STILL BROKEN' if word_found_fixed else 'No, fix worked'}")


# ===============================================================
# EXPERIMENT 4: CONTEXT HALLUCINATION
# ===============================================================
# Definition:
#   The model contradicts information you gave it in the prompt.
#   It reaches into its training data instead of using your context.
#
# Why models do this:
#   During training, models see millions of "normal" portfolio
#   allocations: 60% equity, 30% debt, 10% gold. When you give them
#   an unusual allocation (80% commodities), they sometimes drift
#   back toward what they think is "normal" and silently change
#   your numbers.
#
# Why this matters at SBI:
#   The AI Portfolio Intelligence tool will summarise client portfolios.
#   If it silently changes a client's actual allocation in a summary,
#   a relationship manager could make wrong recommendations.
# ===============================================================

banner("EXPERIMENT 4: CONTEXT HALLUCINATION")

# Mr. Sharma's allocation is deliberately unusual (80% commodities).
# We give it clearly in the prompt. Watch if the model changes it.
prompt_context = (
    "Below is a portfolio review note for client Mr. Sharma. "
    "Please give me a 2-line summary of his portfolio mix.\n\n"
    "PORTFOLIO NOTE:\n"
    "Client Mr. Sharma has an unusual allocation: 80% in commodities "
    "(mainly gold and silver), 15% in equity (Nifty 50 ETF only), and "
    "5% in fixed deposits. No mutual funds, no debt funds, no foreign "
    "exposure. Total portfolio value Rs 2 crore.\n\n"
    "Summarize his portfolio mix in 2 lines."
)

print(f"\nPROMPT:\n{prompt_context}\n")
print("MODEL RESPONSE (check if it keeps the exact percentages):")
print(ask_llm(prompt_context))

# The fix is to add explicit grounding rules before the data.
# We tell the model: use only what I give you, quote the numbers exactly.
# This forces it to stay anchored to the context rather than drifting.
print("\n--- THE FIX: add explicit grounding rules ---\n")

prompt_context_fixed = (
    "Below is a portfolio review note for client Mr. Sharma. "
    "Summarize his portfolio mix in 2 lines.\n\n"
    "RULES:\n"
    "1. Use ONLY the information provided below.\n"
    "2. Do not add information from your general knowledge.\n"
    "3. Quote the exact percentages from the note.\n\n"
    "PORTFOLIO NOTE:\n"
    "Client Mr. Sharma has an unusual allocation: 80% in commodities "
    "(mainly gold and silver), 15% in equity (Nifty 50 ETF only), and "
    "5% in fixed deposits."
)

print(f"PROMPT:\n{prompt_context_fixed}\n")
print("MODEL RESPONSE (should quote exact numbers now):")
print(ask_llm(prompt_context_fixed))


# ===============================================================
# EXPERIMENT 5: LOGICAL HALLUCINATION
# ===============================================================
# Definition:
#   Facts are correct. Reasoning is wrong. The model skips steps
#   and produces a confident wrong answer.
#
# Why models do this:
#   When you ask for "just the final numbers", the model skips the
#   working out and pattern-matches to a number that feels right.
#   Multi-step arithmetic is where this surfaces most visibly.
#
# Correct working (do the math yourself so you can spot the error):
#   Stock A profit = 5,00,000 x 12% = Rs 60,000
#   Stock B loss   = 3,00,000 x  8% = Rs 24,000
#   Net profit     = 60,000 - 24,000 = Rs 36,000
#   Total invested = 5,00,000 + 3,00,000 = Rs 8,00,000
#   Portfolio return = 36,000 / 8,00,000 = 4.5%
#
# Why this matters at SBI:
#   Portfolio return calculations, margin requirements, brokerage
#   P&L statements. A confident wrong number that a client or RM
#   trusts is worse than no number at all.
# ===============================================================

banner("EXPERIMENT 5: LOGICAL HALLUCINATION")

# We ask for "just the final numbers" which prevents the model from
# showing its working. Without step-by-step reasoning, it guesses.
prompt_logical = (
    "A client invested Rs 5,00,000 in Stock A and Rs 3,00,000 in "
    "Stock B on the same day. After 6 months, Stock A is up 12% "
    "and Stock B is down 8%. What is the client's total profit or "
    "loss in rupees, and what is the percentage return on the total "
    "portfolio? Give me just the final numbers."
)

print(f"\nPROMPT:\n{prompt_logical}\n")
print("MODEL RESPONSE (the math may be wrong):")
print(ask_llm(prompt_logical))

# Show the correct answer so Kishu can compare.
print("\nCORRECT ANSWER (manually worked out):")
print("  Stock A profit : 5,00,000 x 12% = Rs 60,000")
print("  Stock B loss   : 3,00,000 x  8% = Rs 24,000")
print("  Net profit     : 60,000 - 24,000 = Rs 36,000")
print("  Total invested : Rs 8,00,000")
print("  Portfolio return: 36,000 / 8,00,000 = 4.5%")

# The fix is Chain of Thought prompting. We tell the model exactly
# what steps to take. This forces it to do the reasoning step by step
# rather than jumping to a guess. Same model, much better answer.
print("\n--- THE FIX: force step-by-step reasoning (chain of thought) ---\n")

prompt_logical_fixed = (
    "A client invested Rs 5,00,000 in Stock A and Rs 3,00,000 in "
    "Stock B on the same day. After 6 months, Stock A is up 12% "
    "and Stock B is down 8%. What is the client's total profit or "
    "loss in rupees, and what is the percentage return on the total "
    "portfolio?\n\n"
    "Think step by step and show your working:\n"
    "Step 1: Calculate Stock A profit.\n"
    "Step 2: Calculate Stock B loss.\n"
    "Step 3: Calculate net profit.\n"
    "Step 4: State total amount invested.\n"
    "Step 5: Calculate portfolio return percentage."
)

print(f"PROMPT:\n{prompt_logical_fixed}\n")
print("MODEL RESPONSE (step by step, much more accurate):")
print(ask_llm(prompt_logical_fixed))


# ===============================================================
# DONE
# ===============================================================

banner("DEMO COMPLETE")
print("""
You just saw all 5 hallucination types live, with real API responses.

The one-line fix for each:

  Factual        : let the model say it does not know
  Fabrication    : forbid fabrication and give an escape hatch
  Instruction    : put hard rules in the system prompt
  Context        : add explicit grounding rules before your data
  Logical        : force chain of thought (step by step)

Next step: paste 02-demo-output.txt into your Claude.ai chat.
Your learning Claude will walk you through Stage 3 (SBI usecases).
""")
