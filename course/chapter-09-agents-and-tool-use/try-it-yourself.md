# Try it yourself: Chapter 9

Three practicals. 30 minutes total. Do them in order.

---

## Practical 1: Give the model a tool and see it decide to use it (8 min)

Open colab.research.google.com and create a new notebook. Paste and run this:

```python
!pip install groq -q
from groq import Groq
from google.colab import userdata
import json

client = Groq(api_key=userdata.get("GROQ_API_KEY"))

# --- DEFINE TOOLS ---
# We describe the tools to the model as a list of JSON schemas.
# The model reads these descriptions and decides when to use them.

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Performs a mathematical calculation. Use this for any arithmetic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to evaluate, e.g. '100 * 0.18' or '(500 + 300) / 4'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_product_info",
            "description": "Looks up information about a product by its name. Returns price and stock status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "The name of the product to look up"
                    }
                },
                "required": ["product_name"]
            }
        }
    }
]

# --- DEFINE THE ACTUAL TOOL FUNCTIONS ---
# These are the real functions your code runs when the model requests a tool call.

def calculate(expression):
    try:
        result = eval(expression)  # Safe here since we control the input
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

def get_product_info(product_name):
    # Simulated product database
    products = {
        "laptop": {"price": 75000, "stock": "in stock", "category": "electronics"},
        "desk chair": {"price": 12000, "stock": "low stock (3 left)", "category": "furniture"},
        "monitor": {"price": 25000, "stock": "out of stock", "category": "electronics"},
        "keyboard": {"price": 3500, "stock": "in stock", "category": "electronics"},
    }
    name = product_name.lower()
    if name in products:
        return products[name]
    return {"error": f"Product '{product_name}' not found"}

# --- AGENT LOOP ---
def run_agent(user_message):
    print(f"\n USER: {user_message}")
    messages = [{"role": "user", "content": user_message}]

    # Keep looping until the model stops calling tools
    while True:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # If no tool was called, we have the final answer
        if not message.tool_calls:
            print(f" AGENT: {message.content}")
            break

        # Otherwise, execute each tool the model requested
        messages.append(message)

        for tool_call in message.tool_calls:
            fn_name = tool_call.function.name
            fn_args = json.loads(tool_call.function.arguments)

            print(f" [TOOL CALL] {fn_name}({fn_args})")

            # Run the actual function
            if fn_name == "calculate":
                result = calculate(**fn_args)
            elif fn_name == "get_product_info":
                result = get_product_info(**fn_args)
            else:
                result = {"error": "Unknown tool"}

            print(f" [TOOL RESULT] {result}")

            # Feed the result back to the model
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

# Test with simple questions
run_agent("What is 18% of 45000?")
run_agent("Is the laptop in stock?")
```

Run it. You will see the model decide to call a tool, your code runs it, the result comes back, and the model uses it to answer.

---

## Practical 2: Multi-step agent reasoning (12 min)

Add a new cell. Now give it questions that require multiple tool calls:

```python
# This requires looking up a product AND doing a calculation
run_agent("What would 3 keyboards cost in total, and what is that with a 10% discount?")

# This requires looking up two products and comparing
run_agent("Is the laptop more expensive than the monitor? By how much?")

# This requires a product lookup followed by a calculation
run_agent("If I buy a desk chair and pay with a Rs 15,000 budget, how much change will I get back?")
```

Run all three. Watch the TOOL CALL and TOOL RESULT lines to see each step the agent takes.

**What to notice:** The model is deciding the sequence of steps on its own. You gave it a goal, not a script. It figured out which tools to call and in what order.

---

## Practical 3: Watch an agent handle a missing tool (10 min)

Add a new cell. Give it a question that requires something it does not have a tool for:

```python
# No weather tool exists
run_agent("What is the weather like in Tokyo right now?")

# No shipping tool exists, but it can still use what it has
run_agent("What is the price of a monitor, and when will it be back in stock?")
```

Run it. For the weather question, the model should acknowledge it cannot get live weather data without a tool for it.

For the monitor question, it can get the price but the database only says "out of stock" with no restock date. See how it handles partial information.

Now try adding a new tool yourself. Add a cell and extend the tools list:

```python
# Add a shipping estimator tool
tools.append({
    "type": "function",
    "function": {
        "name": "get_shipping_estimate",
        "description": "Returns estimated delivery time in days for a given destination city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The destination city"}
            },
            "required": ["city"]
        }
    }
})

# Add the real function
def get_shipping_estimate(city):
    estimates = {
        "mumbai": 1, "delhi": 2, "bangalore": 2,
        "chennai": 3, "kolkata": 3, "hyderabad": 2
    }
    days = estimates.get(city.lower(), 5)
    return {"city": city, "estimated_days": days}

# Update run_agent to handle the new tool
def run_agent_v2(user_message):
    print(f"\n USER: {user_message}")
    messages = [{"role": "user", "content": user_message}]
    while True:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        message = response.choices[0].message
        if not message.tool_calls:
            print(f" AGENT: {message.content}")
            break
        messages.append(message)
        for tool_call in message.tool_calls:
            fn_name = tool_call.function.name
            fn_args = json.loads(tool_call.function.arguments)
            print(f" [TOOL CALL] {fn_name}({fn_args})")
            if fn_name == "calculate":
                result = calculate(**fn_args)
            elif fn_name == "get_product_info":
                result = get_product_info(**fn_args)
            elif fn_name == "get_shipping_estimate":
                result = get_shipping_estimate(**fn_args)
            else:
                result = {"error": "Unknown tool"}
            print(f" [TOOL RESULT] {result}")
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result)})

run_agent_v2("I want to buy a keyboard and ship it to Bangalore. How much will I pay in total and when will it arrive?")
```

Run it. The agent now uses 3 tools in sequence to answer one question.

---

## What to show me before moving to Chapter 10

1. A screenshot showing the multi-step agent using two tools to answer one question
2. A one-line answer to: "What is the difference between a chatbot and an agent?"
