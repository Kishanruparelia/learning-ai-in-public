# Chapter 3: Prompting

**Time needed:** 1 hour
**You will need:** A browser, your Groq API key, Google Colab open

---

## What you will be able to do by the end

1. Write prompts that get useful, specific answers instead of vague ones
2. Use 4 prompting patterns that work across almost every usecase
3. Understand why "be more specific" is not enough advice
4. Spot a weak prompt and rewrite it in under 30 seconds

---

## The big idea

The quality of what you get out of an LLM is almost entirely determined by what you put in.

A vague prompt gets a vague answer. A structured prompt gets a structured answer. This is not magic. The model is predicting what a good continuation looks like, and your prompt is the only signal it has.

Prompting is the skill that separates people who think AI is useless from people who ship real AI products.

---

## What a prompt actually is

A prompt is everything the model sees before it starts generating a reply.

That includes:
- Your question or instruction
- Any context you paste in (documents, data, examples)
- The system prompt (background instructions set by the developer)
- The conversation history so far

The model does not know your intention. It only knows your words. Every mistake in prompting comes from assuming the model understands something you did not write.

---

## The 4 prompting patterns

### Pattern 1: Role + Task + Format

Give the model a role, a specific task, and tell it exactly what format you want back.

**Weak prompt:**
```
Summarise this call transcript
```

**Strong prompt:**
```
You are a call quality analyst at a brokerage firm.
Summarise the following customer service call in exactly 3 bullet points:
one for the customer's problem, one for how the agent handled it, and one
for what should be done differently next time.
```

The strong version has a role (call quality analyst), a task (summarise), and a format (3 bullet points with specific content for each).

### Pattern 2: Few-shot examples

Show the model an example of what good output looks like before asking it to do the real thing.

**Without examples:**
```
Classify this customer message as Complaint, Query, or Compliment.
Message: "Why has my account been blocked without any notice?"
```

**With one example:**
```
Classify customer messages as Complaint, Query, or Compliment.

Example:
Message: "I have been waiting 3 days for my funds to be credited."
Classification: Complaint

Now classify this:
Message: "Why has my account been blocked without any notice?"
Classification:
```

One example is often enough. The model now knows the exact output format you expect.

### Pattern 3: Chain of thought

Ask the model to think step by step before giving the final answer. This dramatically improves accuracy on anything involving reasoning, numbers, or multi-step logic.

**Without chain of thought:**
```
A client has Rs 5,00,000 in Stock A which went up 12%, and Rs 2,00,000
in Stock B which went down 8%. What is the total portfolio return?
```

(The model often gets this wrong, skipping steps and confidently giving a wrong number.)

**With chain of thought:**
```
A client has Rs 5,00,000 in Stock A which went up 12%, and Rs 2,00,000
in Stock B which went down 8%. What is the total portfolio return?

Think step by step:
1. Calculate the profit or loss on Stock A
2. Calculate the profit or loss on Stock B
3. Add them to get total profit or loss
4. Divide by total invested to get the percentage return
5. State the final answer clearly
```

Forcing the reasoning steps catches mistakes before the final answer is generated.

### Pattern 4: Constraints

Tell the model what NOT to do, what length to use, and what to include or exclude.

```
You are an RM assistant at a brokerage.
Write a follow-up message to a client who has not logged in for 30 days.

Rules:
- Maximum 3 sentences
- Do not mention competitors
- Do not use the word "opportunity"
- End with a specific call to action
- Friendly but professional tone
```

Constraints prevent the model from defaulting to generic, bloated, or inappropriate output.

---

## Combining the patterns

The best prompts combine multiple patterns. Here is a complete example:

```
You are a senior relationship manager at SBI Securities. (Role)

A client named Priya has Rs 10 lakh sitting idle in her savings account
linked to her demat. She is 35 years old and has described herself as a
moderate risk investor. She has not invested in the last 6 months. (Context)

Write a WhatsApp message to re-engage her. (Task)

Rules: (Constraints)
- Maximum 4 sentences
- Reference her idle funds
- Suggest one specific action she can take today
- Warm, personal tone. Not salesy.

Example of the tone I want: (Few-shot)
"Hi Ravi, noticed your portfolio has been quiet lately. Markets have been
active and there might be a good moment to revisit your goals. Want to
catch up for 15 minutes this week?"

Now write Priya's message:
```

That prompt will consistently give a better output than any single-line version.

---

## The one mindset shift

Stop thinking of the model as a smart person who just needs a question.

Start thinking of it as a very capable intern who needs exact instructions. The intern does not know your company, your clients, your tone, or what you care about unless you tell them.

Every gap in your prompt is a gap where the model fills in its own assumption. Usually that assumption is wrong.

---

## Now go do the practical

Open `try-it-yourself.md`. You will rewrite weak prompts into strong ones and see the difference in real outputs side by side.

---

## Going deeper (optional)

Open `deep-dive.md` to understand why chain of thought works at a technical level, and how system prompts differ from user prompts.

---

## Check yourself

Open `test.md` before moving to Chapter 4.
