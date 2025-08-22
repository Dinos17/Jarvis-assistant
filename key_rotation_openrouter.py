import os
import asyncio
import httpx
from itertools import cycle
from dotenv import load_dotenv

load_dotenv()

# Load API keys
API_KEYS = [os.getenv(f"OPENROUTER_API_KEY_{i}") for i in range(1, 11)]
MODEL_ID = "qwen/qwen3-235b-a22b:free"
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
MAX_RETRIES = 3
REQUEST_TIMEOUT = 60

async def send_prompt(prompt: str, api_key: str):
    payload = {
        "model": MODEL_ID,
        "messages": [{"role": "user", "content": prompt}]
    }
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        try:
            response = await client.post(
                BASE_URL,
                headers={"Authorization": f"Bearer {api_key}"},
                json=payload
            )
            if response.status_code == 429:
                return None, True
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"], False
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                return None, True
            else:
                raise
        except Exception as e:
            raise RuntimeError(f"Request failed: {e}")

async def main():
    prompt_list = [
        "Hello ARIA, how are you today?",
        "Explain quantum computing in simple terms.",
        "Give me a joke about AI."
    ]
    key_cycle = cycle(API_KEYS)

    for prompt in prompt_list:
        while True:
            api_key = next(key_cycle)
            if not api_key:
                continue
            try:
                answer, rate_limited = await send_prompt(prompt, api_key)
                if rate_limited:
                    print(f"[INFO] Key {api_key[-4:]} reached rate limit, rotating...")
                    continue
                print(f"[Prompt] {prompt}\n[Response] {answer}\n")
                break
            except Exception as e:
                print(f"[ERROR] {e}. Rotating key...")
                continue

if __name__ == "__main__":
    asyncio.run(main())
