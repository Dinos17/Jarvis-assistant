# langchain_memory.py
from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory

class ARIAMemory:
    def __init__(self, user_name: str, context_window: int = 10):
        self.user_name = user_name
        self.context_window = context_window
        self.buffer_memory = ConversationBufferWindowMemory(
            memory_key="chat_history", k=context_window, return_messages=True
        )
        self.summary_memory = ConversationSummaryMemory(
            llm=None,  # optional: can supply an LLM for automatic summarization
            memory_key="chat_history",
            input_key="input",
            return_messages=True
        )

    def load_history(self, history: list):
        for turn in history:
            self.buffer_memory.chat_memory.add_user_message(turn.get("user", ""))
            self.buffer_memory.chat_memory.add_ai_message(turn.get("assistant", ""))

    def get_context(self):
        return {
            "chat_history": self.buffer_memory.load_memory_variables({}).get("chat_history", []),
            "summary": self.summary_memory.load_memory_variables({}).get("chat_history", "")
        }

    def update(self, user_input: str, assistant_output: str):
        self.buffer_memory.chat_memory.add_user_message(user_input)
        self.buffer_memory.chat_memory.add_ai_message(assistant_output)
        # Optional: update summary memory here
