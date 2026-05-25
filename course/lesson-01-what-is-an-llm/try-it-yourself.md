# Try it yourself: Lesson 1

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

You will write 10 lines of code, run them, and get a real AI response. That is it.

### Step 1: Get a free API key (3 min)

1. Go to console.groq.com
2. Sign up with Google (no credit card)
3. Click "API Keys" on the left
4. Click "Create API Key"
5. Copy the key. Save it in a notepad. You will need it in 2 minutes.

### Step 2: Set up your project folder and Python (5 min)

First, let us create a folder where all your AI course work will live.

**On Mac:**

Open Terminal. Type these commands one at a time:

```
cd ~/Desktop
mkdir learning-ai-with-kishan
cd learning-ai-with-kishan
```

**On Windows:**

Open Command Prompt. Type these commands one at a time:

```
cd %USERPROFILE%\Desktop
mkdir learning-ai-with-kishan
cd learning-ai-with-kishan
```

You are now inside your new project folder on your Desktop. Every script you write in this course goes here.

---

Now check if Python is installed. Type:

```
python --version
```

If you see a version number like `Python 3.11.5`, you are good. Skip to Step 3.

If you see an error or "command not found", install Python:

**On Mac:**

Go to python.org/downloads in your browser. Click the big yellow Download button. Open the `.pkg` file and click through the installer. That is it.

**On Windows:**

Go to python.org/downloads. Download the latest Python installer. Run it.

**Important:** on the first screen of the installer, tick the box that says **"Add Python to PATH"** before clicking Install. If you miss this, nothing else will work.

---

After installing, close your Terminal or Command Prompt completely. Open a new one. Navigate back to your folder:

**On Mac:**
```
cd ~/Desktop/learning-ai-with-kishan
```

**On Windows:**
```
cd %USERPROFILE%\Desktop\learning-ai-with-kishan
```

Check the version again:

```
python --version
```

You should now see a version number. On Mac, the command is `python3` not `python`. Use whichever one works for the rest of the lesson and stick with it.

### Step 3: Install the Groq library (1 min)

In terminal:
```
pip install groq
```

Wait for it to finish.

### Step 4: Write your first AI script (5 min)

Open any text editor (Notepad, TextEdit, VS Code, anything). Paste this:

```python
from groq import Groq

client = Groq(api_key="PASTE-YOUR-KEY-HERE")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "Explain how rainbows form, in 3 sentences"}
    ]
)

print(response.choices[0].message.content)
```

Replace `PASTE-YOUR-KEY-HERE` with the API key you copied in Step 1. Keep the quotes.

Save the file as `my-first-ai.py`.

### Step 5: Run it (1 min)

In terminal, navigate to wherever you saved the file. Then type:
```
python my-first-ai.py
```

Wait one second. You should see an explanation of rainbows printed in your terminal.

**Congratulations. You just called an LLM from your own computer.**

### Step 6: Break it on purpose (5 min)

Change the prompt to something the model would not know:
```
What did I have for breakfast today?
```

Run it. Watch what happens. The model might guess, might refuse, might make something up. This is the foundation of Lesson 4 (Hallucinations).

Now change `temperature=0` by editing the call:

```python
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    temperature=0,
    messages=[
        {"role": "user", "content": "Write a 2-line poem about Monday morning"}
    ]
)
```

Run it three times. Notice the output is now identical every time. Temperature 0 means "always pick the most likely next word, no randomness".

Now set `temperature=1.5` and run three times. Notice it gets weirder, more creative, sometimes nonsense.

---

## What to show me before moving to Lesson 2

1. A screenshot of your terminal showing the rainbow explanation
2. A one-line answer to: "Why did temperature 0 give the same output every time?"
