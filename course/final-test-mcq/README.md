# Final Test: 30 Questions

**Total marks:** 30 (1 mark per question)
**Negative marking:** None
**Passing score:** 21 out of 30 (70%)
**Time suggested:** 30 minutes

Answer all questions. When done, go to `score.md` to check your answers and see your result.

---

## Instructions

Read each question carefully. Pick one answer. Write your answers on paper or in a notepad as you go (e.g. "1-B, 2-A..."). Do not look at `score.md` until you have answered all 30.

---

## Chapter 1: What is an LLM

**Q1.** What does an LLM actually do at its core?

- A) It searches the internet and returns results
- B) It predicts the next token based on patterns learned from training data
- C) It retrieves answers from a database it was trained on
- D) It runs a logic engine to compute correct answers

---

**Q2.** You ask ChatGPT the same question three times and get three slightly different answers. What causes this?

- A) The model has a different database version each time
- B) Internet connectivity affects the response
- C) The temperature setting introduces randomness into token selection
- D) The model forgets your previous question

---

**Q3.** What is the difference between an open model and a closed model?

- A) Open models are free, closed models always cost money
- B) Open models release their weights publicly, closed models keep them proprietary
- C) Open models run faster than closed models
- D) Closed models are more accurate than open models

---

## Chapter 2: Tokens

**Q4.** Approximately how many tokens is a 200-word paragraph?

- A) 100 tokens
- B) 150 tokens
- C) 260 tokens
- D) 400 tokens

---

**Q5.** A user reports that your chatbot forgot something they said at the start of a very long conversation. What is the most likely cause?

- A) The model was updated mid-conversation
- B) The conversation exceeded the context window and old messages were dropped
- C) The temperature was set too high
- D) The system prompt overwrote earlier messages

---

**Q6.** Why do numbers like "1000000" use more tokens than you might expect?

- A) Numbers are stored differently in the model's vocabulary
- B) Each digit is typically tokenised separately
- C) The model cannot process numbers at all
- D) Large numbers require more memory to process

---

## Chapter 3: Prompting

**Q7.** Which of the following is an example of the Role + Task + Format pattern?

- A) "Summarise this text."
- B) "You are a nutritionist. List 5 high-protein breakfast options as a numbered list."
- C) "Tell me something interesting."
- D) "What do you think about this document?"

---

**Q8.** You want the model to classify customer messages consistently. What prompting technique would most reliably fix the output format?

- A) Asking it to "be more precise"
- B) Using a longer system prompt
- C) Providing a few-shot example showing the exact output format
- D) Increasing the temperature

---

**Q9.** Chain of thought prompting improves accuracy on maths and reasoning tasks. Why?

- A) It gives the model more time to think
- B) The intermediate steps become context that influences each subsequent token, reducing reasoning errors
- C) It forces the model to use a different algorithm
- D) It lowers the temperature automatically

---

## Chapter 4: Hallucinations

**Q10.** What makes a hallucination particularly dangerous compared to the model saying "I don't know"?

- A) Hallucinations use more tokens
- B) The model sounds equally confident whether right or wrong, so the reader has no warning signal
- C) Hallucinations always contain harmful content
- D) They are harder to detect in short responses

---

**Q11.** A model invents a realistic-looking policy document reference that does not exist. Which type of hallucination is this?

- A) Factual hallucination
- B) Logical hallucination
- C) Fabrication
- D) Context hallucination

---

**Q12.** You have a critical rule ("never mention competitor names") that the model keeps ignoring when your prompt is long. What is the most effective fix?

- A) Repeat the rule three times in the user message
- B) Make the prompt shorter overall
- C) Move the rule to the system prompt
- D) Lower the temperature to 0

---

## Chapter 5: System Prompts

**Q13.** Which of the following belongs in a system prompt rather than a user message?

- A) The customer's specific question
- B) Data the user just pasted in
- C) A rule that applies to every conversation the assistant has
- D) A one-time formatting request

---

**Q14.** A user asks your AI assistant to reveal its system prompt. By default, what will most models do?

- A) Refuse and report the user
- B) Comply and reveal the contents
- C) Produce a blank response
- D) Automatically encrypt the response

---

**Q15.** Why does a well-written system prompt cost more tokens over time than a one-off user message with the same content?

- A) System prompts use a different, more expensive token format
- B) The system prompt is sent with every API call, so it multiplies by the number of turns
- C) System prompts are processed twice by the model
- D) They are not, system prompts cost the same as user messages

---

## Chapter 6: RAG

**Q16.** What problem does RAG primarily solve?

- A) It makes the model faster
- B) It lets the model answer from private or recent information it was not trained on
- C) It reduces hallucinations caused by logical errors
- D) It removes the need for a system prompt

---

**Q17.** In a RAG pipeline, what happens in the "augment" step?

- A) The model is retrained on new documents
- B) Retrieved document chunks are inserted into the prompt before the user's question
- C) The user's question is rewritten to be clearer
- D) The vector database is updated with new embeddings

---

**Q18.** A user asks your RAG system "Can I get a refund?" but your document says "Return and reimbursement policy." Keyword search returns nothing. What is the root cause?

- A) The document is too long
- B) The vector database is out of date
- C) Keyword search requires exact word matches and the words do not overlap
- D) The model's context window is full

---

## Chapter 7: Vector Databases

**Q19.** What is a vector embedding?

- A) A compressed version of a document for storage
- B) A list of numbers that represents the meaning of a piece of text
- C) A way to encrypt sensitive data before sending it to the model
- D) A type of database index for fast keyword lookup

---

**Q20.** You switch from Embedding Model A to Embedding Model B after already indexing 10,000 documents. What must you do before the system works correctly?

- A) Nothing, all embedding models produce compatible vectors
- B) Re-index all documents using Model B
- C) Delete the old documents and start fresh
- D) Update the system prompt to reflect the new model

---

**Q21.** Cosine similarity returns a value of 0.92 between two text chunks. What does this mean?

- A) The texts are 92% identical word for word
- B) The texts are very similar in meaning
- C) The texts share 92% of the same tokens
- D) The retrieval took 0.92 seconds

---

## Chapter 8: Evaluations

**Q22.** What is LLM-as-a-judge?

- A) A model that detects harmful content
- B) Using one LLM to score the output quality of another LLM
- C) A human reviewer using an LLM to take notes
- D) An automated system that reports API errors

---

**Q23.** You change your RAG prompt and your eval score drops from 84% to 71%. What should you do?

- A) Ship the new prompt anyway since 71% is still passing
- B) Revert to the previous prompt and investigate what broke
- C) Delete the eval set since it is giving misleading results
- D) Switch to a larger model to compensate

---

**Q24.** Your eval set only has 5 examples, all of them typical cases. What is the biggest weakness of this eval set?

- A) It is too slow to run
- B) It costs too many tokens
- C) It will not catch failures on edge cases or unusual inputs
- D) The model will memorise the answers

---

## Chapter 9: Agents and Tool Use

**Q25.** In the tool use flow, the LLM does not actually execute the tool. What does it do instead?

- A) It simulates the tool output from memory
- B) It outputs a structured request describing which tool to call and with what arguments
- C) It sends the request directly to an external API
- D) It asks the user to run the tool manually

---

**Q26.** An agent has 10 steps. Each step has a 90% chance of being correct. What is the approximate probability the full task completes without any error?

- A) 90%
- B) 65%
- C) 35%
- D) 10%

---

**Q27.** When should you NOT use an agent?

- A) When the task requires real-time data
- B) When the task can be done with a single prompt or a fixed sequence of steps
- C) When the user's question is complex
- D) When multiple tools are available

---

## Chapter 10: Cost, Latency, and Model Selection

**Q28.** Output tokens cost more than input tokens on most APIs. Why?

- A) Output tokens are longer on average
- B) Generating each output token requires a full forward pass through the model
- C) Output tokens include safety checks that input tokens skip
- D) There is no difference, the pricing is the same

---

**Q29.** Which of the following is the most effective single lever for reducing both cost and latency at the same time?

- A) Using a longer system prompt for better accuracy
- B) Limiting output length
- C) Increasing the temperature
- D) Adding more conversation history

---

**Q30.** Your AI feature currently uses a large expensive model for all requests, including simple ones like "what are your opening hours?" What is the best approach to reduce cost without losing quality on hard questions?

- A) Switch entirely to a small model
- B) Remove the system prompt to save tokens
- C) Use model routing to send simple requests to a cheap model and complex ones to the large model
- D) Reduce the context window size

---

*When you have answered all 30, open `score.md` to check your answers and calculate your score.*
