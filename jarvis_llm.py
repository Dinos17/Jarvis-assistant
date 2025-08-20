import os
import requests
from langchain.llms.base import LLM
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")

class DeepseekLLM(LLM):
    """LangChain-compatible wrapper for Deepseek via OpenRouter."""

    def _call(self, prompt, stop=None):
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek/deepseek-r1-0528:free",
            "messages": [
                {"role": "system", "content": "You are J.A.R.V.I.S., a loyal and intelligent AI assistant."},
                {"role": "user", "content": prompt}
            ]
        }
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[Error: {e}]"

    @property
    def _identifying_params(self):
        return {"api": "Deepseek"}

    @property
    def _llm_type(self):
        return "deepseek"
