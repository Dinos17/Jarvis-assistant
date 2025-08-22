# langchain_memory.py
from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory
from langchain.schema import messages_from_dict, messages_to_dict

class ARIAMemory:
    """
    Handles conversation memory for ARIA using LangChain.
    Combines recent full messages with summarized long-term memory.
    """

    def __init__(self, user_name: str, context_window: int = 8):
        self.user_name = user_name
        self.buffer_memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            k=context_window,
            return_messages=True
        )
        self.summary_memory = ConversationSummaryMemory(
            memory_key="summary",
            llm=None,
            return_messages=True
        )

    def load_history(self, history: list):
        if history:
            self.buffer_memory.chat_memory.messages = messages_from_dict(history)

    def get_context(self):
        return self.summary_memory.load_memory_variables({}) | self.buffer_memory.load_memory_variables({})

    def update(self, user_input: str, assistant_output: str):
        self.buffer_memory.chat_memory.add_user_message(user_input)
        self.buffer_memory.chat_memory.add_ai_message(assistant_output)

    def dump_history(self):
        return messages_to_dict(self.buffer_memory.chat_memory.messages)
