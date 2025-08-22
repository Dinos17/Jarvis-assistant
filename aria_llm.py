# aria_llm.py
import os
import asyncio
import httpx
from personality_aria import get_personality_prompt

MODEL_ID = os.getenv("MODEL_ID", "moonshotai/kimi-k2:free")
API_KEY = os.getenv("OPENROUTER_API_KEY")
TIMEOUT = int(os.getenv("REQUEST_TIMEOUT_SECONDS", 45))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))

class ARIALLM:
    def __init__(self, api_key: str = None, model_id: str = None):
        self.api_key = api_key or API_KEY
        self.model_id = model_id or MODEL_ID

    async def acomplete(self, user_input: str, chat_history: list, user_name: str) -> str:
        system_prompt = get_personality_prompt(user_name)
        payload = {
            "model": self.model_id,
            "messages": [{"role": "system", "content": system_prompt}]
                        + [{"role": "user", "content": msg.get("content", "")} for msg in chat_history]
                        + [{"role": "user", "content": user_input}]
        }

        retries = 0
        while retries <= MAX_RETRIES:
            try:
                async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                    headers = {"Authorization": f"Bearer {self.api_key}"}
                    resp = await client.post("https://openrouter.ai/api/v1/chat/completions",
                                             json=payload, headers=headers)
                    resp.raise_for_status()
                    data = resp.json()
                    return data["choices"][0]["message"]["content"]
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 401:
                    raise ValueError("Unauthorized: Check your API key") from e
                elif e.response.status_code == 429:
                    raise ValueError("Rate limit reached") from e
                else:
                    retries += 1
            except Exception:
                retries += 1
        return "[Error: Failed after retries]"
