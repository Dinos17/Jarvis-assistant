from jarvis_llm import DeepseekLLM
from memory_handler import load_memory, save_memory

# ------------------ Configuration ------------------
CONTEXT_LIMIT = 5  # last N exchanges for context

# ------------------ Initialization ------------------
memory = load_memory()
llm = DeepseekLLM()

print("J.A.R.V.I.S. online. Type 'exit' to shut me down.")

# ------------------ Main Loop ------------------
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        save_memory(memory)
        print("J.A.R.V.I.S.: Shutting down. Goodbye, sir.")
        break

    # Build context prompt
    recent_context = ""
    for entry in memory["chat_history"][-CONTEXT_LIMIT:]:
        recent_context += f"User: {entry['user']}\nJarvis: {entry['jarvis']}\n"

    prompt = recent_context + f"User: {user_input}\nJarvis:"

    # Query Deepseek
    response = llm._call(prompt)
    print(f"J.A.R.V.I.S.: {response}")

    # Save memory
    memory["chat_history"].append({"user": user_input, "jarvis": response})
    save_memory(memory)
