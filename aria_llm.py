import os
import httpx
import asyncio
from dotenv import load_dotenv
from personality_aria import get_personality_prompt

load_dotenv()

# Load single API key for standard ARIA
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY_1")
MODEL_ID = os.getenv("MODEL_ID", "qwen/qwen3-235b-a22b:free")
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "60"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

class ARIALLM:
    """Async wrapper for Qwen3 OpenRouter API."""

    def __init__(self, api_key: str = None, model_id: str = None):
        self.api_key = api_key or OPENROUTER_API_KEY
        self.model_id = model_id or MODEL_ID
        if not self.api_key:
            raise RuntimeError("API key missing. Set OPENROUTER_API_KEY in environment.")

    async def acomplete(self, user_input: str, chat_history: list, user_name: str) -> str:
        system_prompt = get_personality_prompt(user_name)
        payload = {
            "model": self.model_id,
            "messages": [{"role": "system", "content": system_prompt}] + chat_history + [{"role": "user", "content": user_input}]
        }

        delay = 1.0
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
                    resp = await client.post(BASE_URL, headers={"Authorization": f"Bearer {self.api_key}"}, json=payload)
                    if resp.status_code == 429:
                        raise httpx.HTTPStatusError("Rate limit reached", request=resp.request, response=resp)
                    resp.raise_for_status()
                    data = resp.json()
                    return data["choices"][0]["message"]["content"]
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    raise RuntimeError("Rate limit reached for current key")
                if attempt < MAX_RETRIES:
                    await asyncio.sleep(delay)
                    delay *= 2
                    continue
                raise
            except (httpx.TimeoutException, httpx.NetworkError):
                if attempt == MAX_RETRIES:
                    raise RuntimeError("Network error or timeout. Please retry.")
                await asyncio.sleep(delay)
                delay *= 2    def _call(self, prompt, stop=None):
        return asyncio.run(self._acall(prompt))

    @property
    def _identifying_params(self):
        return {"api": "Deepseek"}

    @property
    def _llm_type(self):
        return "deepseek"
