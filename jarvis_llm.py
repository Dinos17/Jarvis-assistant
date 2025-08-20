import os
import asyncio
import httpx
from langchain.llms.base import LLM
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-r1-0528:free"

class DeepseekLLM(LLM):
    """Async LangChain-compatible wrapper for Deepseek."""

    async def _acall(self, prompt, stop=None):
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "You are J.A.R.V.I.S., a loyal and intelligent AI assistant."},
                {"role": "user", "content": prompt}
            ]
        }
        async with httpx.AsyncClient(timeout=30) as client:
            try:
                response = await client.post(BASE_URL, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                return f"[Error: {e}]"

    # For compatibility with LangChain synchronous calls
    def _call(self, prompt, stop=None):
        return asyncio.run(self._acall(prompt))

    @property
    def _identifying_params(self):
        return {"api": "Deepseek"}

    @property
    def _llm_type(self):
        return "deepseek"