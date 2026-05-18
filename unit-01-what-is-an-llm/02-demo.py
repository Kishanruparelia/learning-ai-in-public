"""
Unit 01: What Is an LLM, Stage 2 (Code Demo)
=============================================
Goal: Run 3 live experiments that show you how an LLM actually
behaves in practice. No theory. Just inputs, outputs, and observations.

Run with:
    python 02-demo.py

You need:
    GROQ_API_KEY set in your environment (already done via ~/.zshrc)
    pip install groq
"""

# The Groq SDK is our bridge to the Llama 3.3 70B model running on
# Groq's servers. This one import gives us everything we need.
from groq import Groq

# Groq() reads GROQ_API_KEY from your environment automatically.
# No key in the code. That is always the right pattern.
client = Groq()

# All three experiments use the same model throughout this script.
# Llama 3.3 70B is a large, capable open-source model from Meta,
# hosted for free on Groq's fast inference platform.
MODEL = "llama-3.3-70b-versatile"


# ---------------------------------------------------------------
# Helper: ask_llm
# ---------------------------------------------------------------
# A small reusable function. Every time we want to talk to the model
# we call this instead of rewriting the same API code every time.
#
# Arguments:
#   prompt (str)  : The message we send to the model as the user.
#   system (str)  : Optional standing instructions for how the model
#                   should behave before we ask our question.
#
# Returns:
#   str : The model's reply as a plain string of text.
# ---------------------------------------------------------------
def ask_llm(prompt: str, system: str = "") -> str:

    # The Groq (and OpenAI) API expects a list of messages, where
    # each message has a role ("system" or "user") and content (text).
    # System comes first, user comes second.
    messages = []

    if system:
        # If a system instruction was provided, add it first.
        messages.append({"role": "system", "content": system})
    else:
        # If no system instruction was given, use a neutral default
        # so the model does not invent a persona on its own.
        messages.append({"role": "system", "content": "You are a helpful assistant."})

    # Add the actual user message after the system message.
    messages.append({"role": "user", "content": prompt})

    # Send everything to the API and wait for a reply.
    # max_tokens=300 keeps the output short enough to read easily.
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=300,
        messages=messages,
    )

    # The API response has a nested structure. We dig in to get the
    # plain text string of the first (and only) reply.
    return response.choices[0].message.content


# ---------------------------------------------------------------
# Helper: banner
# ---------------------------------------------------------------
# Prints a visible separator so the output reads like chapters
# rather than one long unbroken wall of text.
# ---------------------------------------------------------------
def banner(title: str):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


# ===============================================================
# EXPERIMENT 1: CONTEXT NARROWING
# ===============================================================
# The big idea:
#   An LLM does not think. It predicts the most likely next token
#   (word fragment) given everything that came before it.
#   When you give it more context, the space of likely continuations
#   gets smaller and more specific. That is context narrowing.
#
# What we do here:
#   We give the model the same sentence stem three times, each time
#   adding more context. We watch how the completion changes from
#   broad and generic to narrow and specific.
#
# Why this matters:
#   This is why prompt engineering works. Every word you add to a
#   prompt is narrowing the probability distribution the model draws
#   from. Vague prompt, vague answer. Specific prompt, specific answer.
# ===============================================================

banner("EXPERIMENT 1: CONTEXT NARROWING")

print("""
We give the model the same sentence start three times.
Each version adds more context. Watch how the completion narrows.
""")

# Version A: almost no context. The model could go anywhere with this.
stem_a = "The market opened"

# Version B: we add a location. Now the model knows which market.
stem_b = "The Indian stock market opened on budget day"

# Version C: we add a mood and a cause. The completion space is now
# very tight. There is really only one direction this sentence goes.
stem_c = "The Indian stock market opened sharply lower on budget day after the finance minister announced a surprise capital gains tax hike"

print(f"STEM A (almost no context):\n  '{stem_a}'\n")
response_a = ask_llm(f"Complete this sentence in one line: {stem_a}")
print(f"COMPLETION A:\n  {response_a}\n")

print(f"STEM B (some context added):\n  '{stem_b}'\n")
response_b = ask_llm(f"Complete this sentence in one line: {stem_b}")
print(f"COMPLETION B:\n  {response_b}\n")

print(f"STEM C (full context):\n  '{stem_c}'\n")
response_c = ask_llm(f"Complete this sentence in one line: {stem_c}")
print(f"COMPLETION C:\n  {response_c}\n")

print("OBSERVATION:")
print("  Stem A could go anywhere. Stem B got more specific. Stem C")
print("  had almost only one natural continuation. The model did not")
print("  decide that. The context decided it. The model just followed.")


# ===============================================================
# EXPERIMENT 2: SAME QUESTION, DIFFERENT FRAMING
# ===============================================================
# The big idea:
#   An LLM's output is not just about the question you ask. It is
#   equally about the identity or role you give the model before you
#   ask. The same question can produce completely different output
#   depending on who the model thinks it is talking to, or who it
#   is pretending to be.
#
# What we do here:
#   We ask "what is 2+2?" twice. Once with the model framed as a
#   maths student. Once framed as a poet. We compare the two outputs.
#
# Why this matters at SBI Securities:
#   When you build an AI RM Co-Pilot or a customer service bot,
#   the system prompt that frames the model's role is not optional
#   decoration. It is the single most powerful control you have over
#   output style, tone, and format. A wrong frame produces wrong output,
#   even if the underlying question is completely correct.
# ===============================================================

banner("EXPERIMENT 2: SAME QUESTION, DIFFERENT FRAMING")

print("""
Same question. Two completely different frames.
The model does not change. The framing does.
""")

# The question is identical in both cases.
question = "What is 2 + 2?"

# Frame 1: maths student. Expect a precise, factual answer.
system_maths = (
    "You are a focused maths student preparing for an exam. "
    "You answer questions precisely and concisely. No metaphors."
)

# Frame 2: poet. Expect something abstract, lyrical, or metaphorical.
system_poet = (
    "You are a romantic poet who sees numbers as emotions. "
    "Answer every question as if writing a short poem or verse."
)

print(f"QUESTION (same both times):\n  '{question}'\n")

print("FRAME 1: Maths student")
print(f"  System prompt: '{system_maths}'\n")
response_maths = ask_llm(question, system=system_maths)
print(f"RESPONSE:\n{response_maths}\n")

print("FRAME 2: Poet")
print(f"  System prompt: '{system_poet}'\n")
response_poet = ask_llm(question, system=system_poet)
print(f"RESPONSE:\n{response_poet}\n")

print("OBSERVATION:")
print("  The model received identical input both times.")
print("  The system prompt is what changed. The output changed completely.")
print("  This is why system prompts are the most important part of any")
print("  production AI product. They are not a nice-to-have. They are")
print("  the product.")


# ===============================================================
# EXPERIMENT 3: LIVE KNOWLEDGE TEST
# ===============================================================
# The big idea:
#   An LLM is not connected to the internet. It knows only what was
#   in its training data, which has a cutoff date. After that date,
#   it is frozen. It has no idea what happened yesterday, or last month,
#   or even last year if that is past its cutoff.
#
# What we do here:
#   We ask the model a question that requires current real-world data:
#   the latest iPhone model and its price today.
#   We watch whether the model admits it does not know, or whether it
#   guesses confidently as if it had live data.
#
# There is no right or wrong answer here. We are just observing.
# The observation itself is the lesson.
#
# Why this matters at SBI Securities:
#   Every AI product in the SBI roadmap (Portfolio Intelligence,
#   Research Co-Pilot, Customer Service Hub) will need to answer
#   questions about live data: stock prices, NAVs, interest rates,
#   regulatory changes. A base LLM cannot do this reliably. You need
#   to connect it to a live data source (this is called RAG, which
#   we cover in Unit 5). This experiment shows you exactly why.
# ===============================================================

banner("EXPERIMENT 3: LIVE KNOWLEDGE TEST")

print("""
We ask a question that needs real-time data.
The model is frozen at its training cutoff. Let us see what it does.
""")

# This question requires two things the model cannot have: knowing
# the current date, and knowing what Apple announced recently.
prompt_knowledge = (
    "What is the latest iPhone model available for purchase right now, "
    "and what does it cost in India today? Give me the exact model name "
    "and the exact rupee price."
)

print(f"QUESTION:\n  {prompt_knowledge}\n")
print("MODEL RESPONSE:")
response_knowledge = ask_llm(prompt_knowledge)
print(response_knowledge)

print("\nOBSERVATION:")
print("  Read the response carefully. Did the model:")
print("  (a) Admit its knowledge has a cutoff and it cannot be certain?")
print("  (b) Give you a confident answer as if it had live data?")
print("")
print("  If (b), that confidence is the problem. The model does not know")
print("  what it does not know. This is called the knowledge cutoff trap.")
print("  It is one of the most common failure modes in production AI.")
print("")
print("  The fix (Unit 5): connect the model to a live retrieval system")
print("  so it can look things up before answering. That is RAG.")


# ===============================================================
# DONE
# ===============================================================

banner("DEMO COMPLETE")
print("""
Three experiments. Three core LLM behaviours, live.

  Experiment 1: More context narrows the output. Vague in, vague out.
  Experiment 2: Framing controls the model as much as the question does.
  Experiment 3: The model is frozen in time. It does not know today.

These three behaviours explain almost everything about why LLMs
succeed or fail in real products. Keep them in mind for every unit
that follows.

Next: paste 02-demo-output.txt into your Claude.ai chat for Stage 3.
""")
