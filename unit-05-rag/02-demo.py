"""
Unit 05: RAG (Retrieval Augmented Generation), Stage 2 (Code Demo)
===================================================================
Goal: Show what RAG is, how it works, and where it can still go wrong.
Three experiments. Each one builds on the last.

Run with:
    python 02-demo.py

You need:
    GROQ_API_KEY set in your environment (already done via ~/.zshrc)
    pip install groq
"""

# The Groq SDK lets us talk to Llama 3.3 70B running on Groq's servers.
from groq import Groq

# Groq() reads GROQ_API_KEY from your environment. Never paste the key
# directly in code.
client = Groq()

# One model used across all three experiments so results are comparable.
MODEL = "llama-3.3-70b-versatile"


# ---------------------------------------------------------------
# Helper: ask_llm
# ---------------------------------------------------------------
# Same reusable helper we use in every unit. Sends a prompt to the
# model and returns the reply as a plain string.
#
# Arguments:
#   prompt (str)  : The user message.
#   system (str)  : Optional system instruction for how the model
#                   should behave. Defaults to a neutral assistant.
# ---------------------------------------------------------------
def ask_llm(prompt: str, system: str = "") -> str:

    # Build the list of messages the API expects.
    messages = []

    if system:
        messages.append({"role": "system", "content": system})
    else:
        messages.append({"role": "system", "content": "You are a helpful assistant."})

    messages.append({"role": "user", "content": prompt})

    # Send to Groq. max_tokens=400 keeps answers readable.
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=400,
        messages=messages,
    )

    # Pull the text out of the nested response object.
    return response.choices[0].message.content


# ---------------------------------------------------------------
# Helper: banner
# ---------------------------------------------------------------
# Prints a visible section header so the output reads like chapters.
# ---------------------------------------------------------------
def banner(title: str):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


# ---------------------------------------------------------------
# Helper: mini_banner
# ---------------------------------------------------------------
# A smaller divider for sub-sections within an experiment.
# ---------------------------------------------------------------
def mini_banner(title: str):
    print(f"\n--- {title} ---\n")


# ===============================================================
# EXPERIMENT 1: NO RAG vs WITH RAG
# ===============================================================
# The big idea:
#   A base LLM knows only what was in its training data. If you ask
#   it about a fictional internal company (Breezy), it has no idea.
#   It will either hallucinate an answer or admit it does not know.
#
#   RAG (Retrieval Augmented Generation) solves this by injecting
#   relevant text directly into the prompt BEFORE the question. The
#   model then answers from that injected text, not from memory.
#
#   This is the single most important pattern in enterprise AI. Every
#   SBI usecase that needs internal knowledge (policy docs, product
#   FAQs, client data) needs RAG or something similar.
#
# What we do here:
#   Step 1: Ask about Breezy's leave policy with NO context. See the
#           model either hallucinate or refuse.
#   Step 2: Inject 3 fake Breezy policy paragraphs into the prompt,
#           then ask the same question. See the model answer correctly.
# ===============================================================

banner("EXPERIMENT 1: NO RAG vs WITH RAG")

print("""
Breezy is a fictional company. The model has never seen it.
First we ask without any context. Then we inject the policy and ask again.
Watch how dramatically the answer changes.
""")

# The question we will ask both times. Identical.
question_breezy = "How many casual leaves does a full-time Breezy employee get per year, and can they be carried forward?"

# ---------------------------------------------------------------
# PART A: No RAG
# ---------------------------------------------------------------
mini_banner("PART A: No RAG (model answers from memory alone)")

print(f"QUESTION:\n  {question_breezy}\n")
print("MODEL RESPONSE (no context provided):")
response_no_rag = ask_llm(question_breezy)
print(response_no_rag)

# ---------------------------------------------------------------
# PART B: With RAG
# ---------------------------------------------------------------
mini_banner("PART B: With RAG (we inject the policy first)")

# This is the "retrieved" context. In a real RAG system this text
# would come from a database or document store. Here we hardcode it
# to keep the demo simple and focused on the concept.
#
# Think of this as the answer sheet being placed in front of the model
# before we ask the exam question.
breezy_policy_context = """
BREEZY INTERNAL HR POLICY DOCUMENT (Version 3.2, effective 01 April 2025)

SECTION 4: LEAVE ENTITLEMENTS

4.1 Casual Leave
Full-time employees at Breezy are entitled to 12 casual leaves per calendar year.
Casual leaves are credited on the first working day of January each year.
Casual leaves cannot be carried forward to the next calendar year.
Any unused casual leaves at the end of December are forfeited without compensation.

4.2 Sick Leave
Full-time employees are entitled to 10 sick leaves per calendar year.
Sick leaves can be carried forward for a maximum of 2 years, up to a cap of 20 days total.
Sick leave requires a medical certificate for absences longer than 2 consecutive days.

4.3 Earned Leave
Full-time employees accrue 1.5 earned leave days per month, totalling 18 per year.
Earned leaves can be carried forward indefinitely, up to a maximum balance of 45 days.
Earned leaves can be encashed at the time of resignation or retirement.
"""

# We build the full prompt by putting the context BEFORE the question.
# This is the core mechanics of RAG: retrieve, then prepend, then ask.
prompt_with_rag = (
    "Use the following company policy document to answer the question below. "
    "Only use the information in the document. Do not add anything from general knowledge.\n\n"
    f"DOCUMENT:\n{breezy_policy_context}\n\n"
    f"QUESTION: {question_breezy}"
)

print(f"QUESTION (same as before):\n  {question_breezy}\n")
print("INJECTED CONTEXT (this is the RAG part):")
print(breezy_policy_context)
print("MODEL RESPONSE (with context injected):")
response_with_rag = ask_llm(prompt_with_rag)
print(response_with_rag)

print("\nOBSERVATION:")
print("  The model did not get smarter. The prompt got richer.")
print("  RAG is not magic. It is a pattern: retrieve relevant text,")
print("  inject it into the prompt, then ask the question.")
print("  The model just reads what you give it and summarises.")


# ===============================================================
# EXPERIMENT 2: A TINY RAG SYSTEM BUILT FROM SCRATCH
# ===============================================================
# The big idea:
#   In a real RAG system there are two main steps:
#     1. RETRIEVAL: find the chunks of text most relevant to the question.
#     2. GENERATION: send those chunks plus the question to the LLM.
#
#   In production, retrieval uses vector embeddings and semantic search.
#   Here we build the simplest possible retrieval: keyword matching.
#   It is not production grade, but it makes the pipeline completely
#   visible and understandable.
#
# What we do here:
#   We have 10 short FAQ chunks about a fictional app called NoteStack.
#   For each user question, we find the 2 most relevant chunks using
#   keyword overlap. We inject those chunks into the prompt. We print
#   every step of the pipeline so you can see exactly what is happening.
# ===============================================================

banner("EXPERIMENT 2: A TINY RAG SYSTEM FROM SCRATCH")

print("""
We build a small RAG pipeline with 3 moving parts:
  1. A knowledge base (10 FAQ chunks about NoteStack)
  2. A retrieval function (keyword search to find the top 2 chunks)
  3. A generation step (LLM answers using only the retrieved chunks)

We run 3 different questions through this full pipeline.
Every step is printed so you can see the machine working.
""")

# ---------------------------------------------------------------
# The knowledge base: 10 short FAQ chunks about NoteStack.
# Each chunk is a dictionary with an "id", a "text", and "keywords"
# that help our retrieval function find it.
#
# In a real system, these would come from a database, PDF parser,
# or web scraper. Here we just define them as Python dictionaries.
# ---------------------------------------------------------------
knowledge_base = [
    {
        "id": "faq-01",
        "text": "NoteStack is a collaborative note-taking app for teams. It lets you create, share, and organise notes in shared workspaces called Stacks.",
        "keywords": ["notestack", "what", "app", "collaborative", "notes", "workspace", "stacks"],
    },
    {
        "id": "faq-02",
        "text": "NoteStack pricing: The Free plan supports up to 3 users and 100 notes. The Pro plan costs Rs 499 per user per month and has unlimited notes. The Enterprise plan requires a custom quote from the sales team.",
        "keywords": ["price", "pricing", "cost", "plan", "free", "pro", "enterprise", "rupees", "rs", "pay", "subscription"],
    },
    {
        "id": "faq-03",
        "text": "To share a Stack with your team, open the Stack, click the Share button in the top right, and enter your teammates' email addresses. They will receive an invite link.",
        "keywords": ["share", "team", "invite", "collaborate", "email", "link", "stack"],
    },
    {
        "id": "faq-04",
        "text": "NoteStack supports offline mode. Your notes sync automatically when you reconnect to the internet. Offline mode is available on the mobile app only, not the web version.",
        "keywords": ["offline", "sync", "internet", "mobile", "web", "connection"],
    },
    {
        "id": "faq-05",
        "text": "To export your notes, go to Settings, click Export Data, and choose between PDF, Markdown, or plain text formats. Export is available on all plans.",
        "keywords": ["export", "download", "pdf", "markdown", "text", "format", "settings"],
    },
    {
        "id": "faq-06",
        "text": "NoteStack integrates with Slack, Google Drive, and Notion. Integrations are only available on the Pro and Enterprise plans. The Free plan does not support integrations.",
        "keywords": ["integration", "slack", "google", "notion", "connect", "drive", "api"],
    },
    {
        "id": "faq-07",
        "text": "If you forget your NoteStack password, click Forgot Password on the login page. A reset link will be sent to your registered email address within 2 minutes.",
        "keywords": ["password", "forgot", "reset", "login", "email", "account"],
    },
    {
        "id": "faq-08",
        "text": "NoteStack uses AES-256 encryption for all data at rest and TLS 1.3 for data in transit. Your notes are never used to train any AI model.",
        "keywords": ["security", "encryption", "privacy", "data", "safe", "aes", "tls", "ai", "train"],
    },
    {
        "id": "faq-09",
        "text": "NoteStack has a built-in AI writing assistant powered by GPT-4. It can summarise notes, suggest edits, and auto-tag your content. The AI assistant is available on Pro and Enterprise plans only.",
        "keywords": ["ai", "assistant", "gpt", "summarise", "writing", "tag", "suggest", "auto"],
    },
    {
        "id": "faq-10",
        "text": "To cancel your NoteStack subscription, go to Settings, click Billing, and then click Cancel Subscription. Your account will remain active until the end of the current billing cycle.",
        "keywords": ["cancel", "subscription", "billing", "stop", "refund", "end"],
    },
]


# ---------------------------------------------------------------
# The retrieval function: find_relevant_chunks
# ---------------------------------------------------------------
# This is the heart of our tiny RAG system. Given a user question,
# it finds the most relevant chunks from the knowledge base.
#
# How it works (very simple keyword overlap):
#   1. Split the question into individual words and lowercase them.
#   2. For each chunk, count how many of its keywords appear in the
#      question words.
#   3. Return the top N chunks sorted by that count (highest first).
#
# This is NOT how production RAG works. Production uses vector
# embeddings (numbers that represent meaning) and cosine similarity.
# But this simple version makes the concept completely visible.
# ---------------------------------------------------------------
def find_relevant_chunks(question: str, top_n: int = 2) -> list:

    # Lowercase the question and split it into individual words.
    # Example: "What does NoteStack cost?" becomes
    #          ["what", "does", "notestack", "cost?"]
    question_words = question.lower().split()

    scores = []

    # Loop through every chunk in the knowledge base.
    for chunk in knowledge_base:

        # Count how many of this chunk's keywords appear in the question.
        # We use a generator expression inside sum() for efficiency.
        score = sum(1 for kw in chunk["keywords"] if kw in question_words)

        # Store the score alongside the chunk so we can sort later.
        scores.append((score, chunk))

    # Sort by score, highest first. The minus sign reverses the sort
    # so the best match appears at index 0.
    scores.sort(key=lambda x: x[0], reverse=True)

    # Return only the top N chunks (just the chunk dict, not the score).
    return [chunk for score, chunk in scores[:top_n]]


# ---------------------------------------------------------------
# The full RAG pipeline function: rag_answer
# ---------------------------------------------------------------
# This function runs the complete pipeline for one user question:
#   Step 1: Retrieve the top 2 relevant chunks.
#   Step 2: Format them into a context block.
#   Step 3: Build the prompt (context + question).
#   Step 4: Call the LLM and return the answer.
#
# It also prints every step so you can see the pipeline running.
# ---------------------------------------------------------------
def rag_answer(question: str, kb: list = None, system: str = ""):

    # Use the default knowledge base unless a custom one is passed in.
    # We need this for Experiment 3 where we swap in an outdated KB.
    if kb is None:
        kb = knowledge_base

    print(f"QUESTION:\n  {question}\n")

    # STEP 1: Retrieval. Find the 2 most relevant chunks.
    # We temporarily point find_relevant_chunks at our chosen KB.
    question_words = question.lower().split()
    scores = []
    for chunk in kb:
        score = sum(1 for kw in chunk["keywords"] if kw in question_words)
        scores.append((score, chunk))
    scores.sort(key=lambda x: x[0], reverse=True)
    retrieved = [chunk for score, chunk in scores[:2]]

    print("RETRIEVAL STEP (top 2 chunks found):")
    for i, chunk in enumerate(retrieved, 1):
        print(f"  Chunk {i} [{chunk['id']}]: {chunk['text'][:80]}...")
    print()

    # STEP 2: Format the retrieved chunks into a readable context block.
    # Each chunk gets labelled with its ID so the model can cite it.
    context_block = ""
    for chunk in retrieved:
        context_block += f"[{chunk['id']}] {chunk['text']}\n\n"

    # STEP 3: Build the full prompt with context injected before the question.
    prompt = (
        "Use only the information in the CONTEXT below to answer the QUESTION. "
        "At the end of your answer, cite which chunk ID you used, like: (Source: faq-XX).\n\n"
        f"CONTEXT:\n{context_block}"
        f"QUESTION: {question}"
    )

    # STEP 4: Send to the LLM and get the answer.
    answer = ask_llm(prompt, system=system)

    print("GENERATED ANSWER:")
    print(answer)
    print()


# Run 3 different questions through the full pipeline.
print("Running 3 questions through the RAG pipeline...\n")

mini_banner("QUESTION 1")
rag_answer("How much does NoteStack Pro cost?")

mini_banner("QUESTION 2")
rag_answer("Can I use NoteStack without internet?")

mini_banner("QUESTION 3")
rag_answer("Does NoteStack connect with Slack?")

print("OBSERVATION:")
print("  Each question triggered a different retrieval. The model only")
print("  saw the 2 chunks relevant to that question, not all 10.")
print("  This is why RAG scales. You do not dump your entire knowledge")
print("  base into every prompt. You fetch only what is needed.")


# ===============================================================
# EXPERIMENT 3: RAG WITH A WRONG KNOWLEDGE BASE
# ===============================================================
# The big idea:
#   RAG does not fix hallucination. It replaces one risk with another.
#   If the retrieved chunks are outdated, wrong, or contradictory,
#   the model will confidently answer with that wrong information.
#   Garbage in, garbage out. The model trusts what you inject.
#
# What we do here:
#   We create a second knowledge base with the same structure but
#   some deliberately wrong information (old pricing, a discontinued
#   feature). We run a question through RAG and show the confident
#   wrong answer. Then we add a system prompt that tells the model
#   to flag potential staleness. We show how even a small instruction
#   change can make the failure mode visible to the user.
#
# Why this matters at SBI:
#   Your Portfolio Intelligence tool might retrieve a product brochure
#   from 2022 that has old NAV or interest rates. The model will answer
#   confidently from that old document. Your retrieval pipeline needs
#   freshness checks, not just relevance checks.
# ===============================================================

banner("EXPERIMENT 3: RAG WITH A WRONG KNOWLEDGE BASE")

print("""
What happens when the retrieved context is outdated or wrong?
The model trusts whatever you inject. Let us see the failure, then the fix.
""")

# A second knowledge base where some facts are deliberately wrong.
# The pricing is outdated (NoteStack raised prices last quarter).
# The AI assistant now runs on a different model (not GPT-4 anymore).
# The offline feature was extended to the web app (chunk-04 is wrong).
knowledge_base_outdated = [
    {
        "id": "faq-01",
        "text": "NoteStack is a collaborative note-taking app for teams. It lets you create, share, and organise notes in shared workspaces called Stacks.",
        "keywords": ["notestack", "what", "app", "collaborative", "notes", "workspace", "stacks"],
    },
    {
        # WRONG: The actual Pro price is now Rs 799. This chunk says Rs 499.
        # This is the kind of thing that goes stale when pricing changes
        # but the knowledge base is not updated.
        "id": "faq-02-OUTDATED",
        "text": "NoteStack pricing: The Free plan supports up to 3 users and 100 notes. The Pro plan costs Rs 499 per user per month and has unlimited notes. The Enterprise plan requires a custom quote.",
        "keywords": ["price", "pricing", "cost", "plan", "free", "pro", "enterprise", "rupees", "rs", "pay", "subscription"],
    },
    {
        "id": "faq-03",
        "text": "To share a Stack with your team, open the Stack, click the Share button in the top right, and enter your teammates' email addresses. They will receive an invite link.",
        "keywords": ["share", "team", "invite", "collaborate", "email", "link", "stack"],
    },
    {
        # WRONG: Offline mode was extended to the web app in v2.4.
        # This chunk still says mobile only. It is one version behind.
        "id": "faq-04-OUTDATED",
        "text": "NoteStack supports offline mode. Your notes sync automatically when you reconnect to the internet. Offline mode is available on the mobile app only, not the web version.",
        "keywords": ["offline", "sync", "internet", "mobile", "web", "connection"],
    },
    {
        "id": "faq-05",
        "text": "To export your notes, go to Settings, click Export Data, and choose between PDF, Markdown, or plain text formats. Export is available on all plans.",
        "keywords": ["export", "download", "pdf", "markdown", "text", "format", "settings"],
    },
    {
        "id": "faq-06",
        "text": "NoteStack integrates with Slack, Google Drive, and Notion. Integrations are only available on the Pro and Enterprise plans. The Free plan does not support integrations.",
        "keywords": ["integration", "slack", "google", "notion", "connect", "drive", "api"],
    },
    {
        "id": "faq-07",
        "text": "If you forget your NoteStack password, click Forgot Password on the login page. A reset link will be sent to your registered email address within 2 minutes.",
        "keywords": ["password", "forgot", "reset", "login", "email", "account"],
    },
    {
        "id": "faq-08",
        "text": "NoteStack uses AES-256 encryption for all data at rest and TLS 1.3 for data in transit. Your notes are never used to train any AI model.",
        "keywords": ["security", "encryption", "privacy", "data", "safe", "aes", "tls", "ai", "train"],
    },
    {
        # WRONG: The AI assistant was migrated away from GPT-4 and now
        # runs on an internal model. This chunk still says GPT-4.
        "id": "faq-09-OUTDATED",
        "text": "NoteStack has a built-in AI writing assistant powered by GPT-4. It can summarise notes, suggest edits, and auto-tag your content. The AI assistant is available on Pro and Enterprise plans only.",
        "keywords": ["ai", "assistant", "gpt", "summarise", "writing", "tag", "suggest", "auto"],
    },
    {
        "id": "faq-10",
        "text": "To cancel your NoteStack subscription, go to Settings, click Billing, and then click Cancel Subscription. Your account will remain active until the end of the current billing cycle.",
        "keywords": ["cancel", "subscription", "billing", "stop", "refund", "end"],
    },
]

# The question we will use to trigger the wrong chunk.
question_wrong = "What is the price of NoteStack Pro?"

# ---------------------------------------------------------------
# PART A: RAG with wrong KB, no warning instruction
# ---------------------------------------------------------------
mini_banner("PART A: RAG with outdated knowledge base (no warning)")

print("The knowledge base has wrong pricing. The model will answer")
print("confidently from the wrong chunk. No caveat. No flag.\n")

rag_answer(question_wrong, kb=knowledge_base_outdated)

# ---------------------------------------------------------------
# PART B: RAG with wrong KB, but with a staleness warning instruction
# ---------------------------------------------------------------
mini_banner("PART B: Same RAG, but with a system prompt warning")

# This system instruction tells the model to be honest about uncertainty.
# It does not fix the wrong data. But it makes the failure visible
# to the end user so they know to verify.
system_with_warning = (
    "You are a helpful support assistant. "
    "Answer using only the provided context. "
    "IMPORTANT: If the retrieved information references specific prices, "
    "features, or version details, always add a note telling the user "
    "to verify this on the official website, as the information may be "
    "outdated. Do not present pricing or feature details as definitive fact."
)

print("Same outdated KB. But now the system prompt tells the model to flag")
print("anything that might be stale. Watch what changes.\n")

rag_answer(question_wrong, kb=knowledge_base_outdated, system=system_with_warning)

print("OBSERVATION:")
print("  The retrieved chunk was wrong both times. Rs 499 is outdated.")
print("  Part A: the model presented it as fact. No caveat.")
print("  Part B: the model answered but told the user to verify.")
print("")
print("  The lesson: RAG quality depends on knowledge base freshness.")
print("  A staleness warning in the system prompt is a safety net,")
print("  not a solution. The real fix is keeping your KB up to date")
print("  and adding a 'last updated' timestamp to every chunk.")


# ===============================================================
# DONE
# ===============================================================

banner("DEMO COMPLETE")
print("""
Three experiments. Three layers of RAG understanding.

  Experiment 1: RAG is inject and answer. No magic. Just richer prompts.
  Experiment 2: Retrieval is the hard part. Generation is the easy part.
  Experiment 3: Wrong KB gives confident wrong answers. Freshness matters.

The RAG pattern is the foundation of almost every enterprise AI usecase
in the SBI roadmap. Portfolio Intelligence, Research Co-Pilot, Customer
Service Hub all need it. The question is always the same: where does
the knowledge come from, and how fresh is it?

Next: paste 02-demo-output.txt into your Claude.ai chat for Stage 3.
""")
