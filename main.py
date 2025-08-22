import asyncio
from langchain_memory import ARIAMemory
from aria_llm import ARIALLM

CONTEXT_LIMIT = 8

async def main():
    user_name = input("Hello! What is your name? ").strip()
    memory = ARIAMemory(user_name=user_name, context_window=CONTEXT_LIMIT)
    llm = ARIALLM()

    print(f"ARIA online. Type 'exit' to shut me down, {user_name}.")

    while True:
        try:
            user_input = input(f"{user_name}: ").strip()
        except (KeyboardInterrupt, EOFError):
            user_input = "exit"

        if user_input.lower() in {"exit", "quit"}:
            print(f"ARIA: Goodbye, {user_name}. Shutting down.")
            break

        context = memory.get_context()
        try:
            reply = await llm.acomplete(user_input, context.get("chat_history", []), user_name)
        except Exception as e:
            reply = f"[Error] {e}"

        print(f"ARIA: {reply}")
        memory.update(user_input, reply)

if __name__ == "__main__":
    asyncio.run(main())
