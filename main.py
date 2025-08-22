# main.py
import asyncio
from aria_llm import ARIALLM
from langchain_memory import ARIAMemory
import os

async def main():
    user_name = input("Hello! What is your name? ").strip()
    memory = ARIAMemory(user_name)
    llm = ARIALLM()

    print(f"\nARIA online. Type 'exit' to shut me down, {user_name}.\n")

    while True:
        try:
            user_input = input(f"{user_name}: ").strip()
            if user_input.lower() in ("exit", "quit"):
                print("Shutting down ARIA...")
                break

            context = memory.get_context()
            response = await llm.acomplete(user_input, context["chat_history"], user_name)
            print(f"ARIA: {response}\n")

            memory.update(user_input, response)
        except KeyboardInterrupt:
            print("\nShutting down ARIA...")
            break
        except Exception as e:
            print(f"[Error] {e}\n")

if __name__ == "__main__":
    asyncio.run(main())
