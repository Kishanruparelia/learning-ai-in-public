# Try it yourself: Chapter 1

Three practicals. 30 minutes total. Do them in order.

---

## Practical 1: Talk to ChatGPT like a human (5 min)

Open chatgpt.com (free, no signup needed for basic chat).

Type exactly this:
```
Explain how a microwave works to a 7-year-old
```

Read the answer. Now type:
```
Now explain it to a physics professor
```

Notice it changed style, vocabulary, depth. Same topic, two different audiences. The LLM is predicting words that fit the new context.

**What this proves:** the model is not pulling answers from a library. It is generating text that fits the situation you describe.

---

## Practical 2: Watch the randomness (5 min)

Still in ChatGPT. Type this exact prompt three times in three new chats:
```
Write a 2-line poem about Monday morning
```

You will get three different poems.

Now you understand why two people asking the same AI the same question get different answers. There is built-in randomness.

---

## Practical 3: Run your first LLM call from code (20 min)

This is where most courses lose people. We are not going to lose you.

No installs. No terminal. Everything runs in your browser using Google Colab, a free tool from Google. All you need is a Google account.

### Step 1: Get a free API key (3 min)

1. Go to console.groq.com
2. Sign in with Google (no credit card needed)
3. Click "API Keys" on the left sidebar
4. Click "Create API Key"
5. Give it any name, like "my-first-key"
6. Copy the key. It looks like a long string of random letters. Save it in a notepad for now.

### Step 2: Open Google Colab (1 min)

1. Go to colab.research.google.com
2. Sign in with your Google account
3. Click "New notebook" in the top left

You will see a blank page with an empty box. That box is called a cell. It is where you write and run code.

### Step 3: Save your API key safely (2 min)

You should never paste your API key directly into code. If you share the notebook, anyone can see it and use your key.

Colab has a built-in safe place for keys called Secrets.

1. On the left sidebar, click the key icon (it looks like a small key)
2. Click "Add new secret"
3. In the Name field, type: `GROQ_API_KEY`
4. In the Value field, paste the key you copied in Step 1
5. Toggle the switch to on so this notebook can access it
6. Click the X to close the panel

Your key is now stored safely. The code will read it from there, not from the visible cell.

### Step 4: Install Groq and run your first AI call (5 min)

Click inside the empty cell. Paste this entire block:

```python
# Install the Groq library (only needed once per session)
!pip install groq -q

# Import the library and the tool that reads your secret key
from groq import Groq
from google.colab import userdata

# Create a connection to the Groq API using your saved key
client = Groq(api_key=userdata.get("GROQ_API_KEY"))

# Send a message to the AI and store the response
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "Explain how rainbows form, in 3 sentences"}
    ]
)

# Print what the AI said
print(response.choices[0].message.content)
```

Now press **Shift + Enter** to run it. Wait about 5 seconds.

You should see an explanation of rainbows appear below the cell.

**Congratulations. You just called an LLM from your browser.**

### Step 5: Break it on purpose (5 min)

Change the prompt inside the quotes to:
```
What did I have for breakfast today?
```

Press Shift + Enter again. Watch what happens. The model might guess, might refuse, might make something up. This is the foundation of Chapter 4 (Hallucinations).

Now add `temperature=0` to the call, like this:

```python
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    temperature=0,
    messages=[
        {"role": "user", "content": "Write a 2-line poem about Monday morning"}
    ]
)
print(response.choices[0].message.content)
```

Run it three times by pressing Shift + Enter three times. Notice the output is identical every time. Temperature 0 means "always pick the most likely next word, no randomness".

Now change `temperature=0` to `temperature=1.5` and run three times. Notice it gets weirder, more creative, sometimes nonsense.

---

## What to show me before moving to Chapter 2

1. A screenshot of your Colab notebook showing the rainbow explanation
2. A one-line answer to: "Why did temperature 0 give the same output every time?"
