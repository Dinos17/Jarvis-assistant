# ARIA — Artificial Realistic Intelligence Agent

**ARIA** is a modular, async conversational assistant powered by OpenRouter-hosted AI models (default: `qwen/qwen3-235b-a22b:free`). It remembers long interactions using LangChain memory, has a customizable personality, and can rotate API keys to avoid rate limits. ARIA is lightweight enough for Replit and performant on your local PC.

---

## 🚀 Features

- **Personalized Conversation:** ARIA learns your name, simulates emotion-aware replies, and has a configurable personality (`personality_aria.py`).
- **Long-term Memory:** Remembers conversations using LangChain buffer and summary memory (`langchain_memory.py`).
- **Reliable Async API:** Fast, resilient OpenRouter LLM client with retries and backoff (`aria_llm.py`).
- **API Key Rotation:** Easily scale up requests without hitting rate limits (`key_rotation_openrouter.py`).
- **Simple CLI:** Talk to ARIA in your terminal (`main.py`).
- **Easy Config:** Tune everything with a `.env` file — models, timeouts, keys, and more.
- **Replit & Local Ready:** No virtual environment required, works out-of-the-box on Replit or your own machine.

---

## 🧩 Architecture Overview

```
User CLI <--> main.py
                 |
                 +--> langchain_memory.py        # Memory: buffer + summary
                 +--> aria_llm.py                # Async OpenRouter LLM client
                 +--> personality_aria.py        # System prompt/personality
                 +--> key_rotation_openrouter.py # Batch key rotation utility
```

- **main.py:** Orchestrates CLI, memory, and LLM interactions.
- **langchain_memory.py:** Tracks conversation history smartly.
- **aria_llm.py:** Sends prompts to any OpenRouter model.
- **personality_aria.py:** Sets ARIA’s tone and behavioral rules.
- **key_rotation_openrouter.py:** For high-volume/batch requests.

---

## 📄 File Guide

### `.env` — Secrets & Settings
```env
OPENROUTER_API_KEY=sk-or-your-primary-key          # For single-key mode
OPENROUTER_API_KEY_1=sk-or-key1                    # For key rotation (add up to 10)
...
OPENROUTER_API_KEY_10=sk-or-key10
MODEL_ID=qwen/qwen3-235b-a22b:free                 # Default model
CONTEXT_LIMIT=8                                    # Chat buffer size
REQUEST_TIMEOUT_SECONDS=60
MAX_RETRIES=3
```
> ⚠️ **Never commit your `.env` file!**

---

### `personality_aria.py`
- Returns the system prompt: how ARIA should sound, behave, and address you.

### `langchain_memory.py`
- Combines buffer and summary memory for efficient, realistic chat history.

### `aria_llm.py`
- Async LLM client with robust error/retry handling.
- Reads your model and key from `.env`.

### `main.py`
- CLI entry point. Handles user input, memory, and LLM calls.

### `key_rotation_openrouter.py`
- For batch prompts. Automatically rotates through multiple API keys.

---

## 🛠️ Installation

### Quick Start (Replit)

1. **Create a new Repl** (Python).
2. **Copy project files** into your Repl.
3. **Add secrets**: Set `OPENROUTER_API_KEY` (or multiple for rotation), plus other `.env` keys.
4. **Install packages:**  
   `pip install httpx python-dotenv langchain`
5. **Run:**  
   `python main.py`

---

### Local Installation

1. **Clone this repo**.
2. *(Optional)* Create a venv:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install httpx python-dotenv langchain
   ```
4. **Create a `.env` file** (see template above).
5. **Run:**
   ```bash
   python main.py
   ```

---

## 💬 Usage Example

```bash
python main.py
```

```
Hello! What is your name? Dino
ARIA online. Type 'exit' to shut me down, Dino.
Dino: hi ARIA
ARIA: Hello, Dino! How's your day going so far?
Dino: remind me about the meeting tomorrow
ARIA: Got it, Dino — when is the meeting scheduled?
```

**For batch jobs:**
```bash
python key_rotation_openrouter.py
```

---

## 🔄 How Key Rotation Works

1. Loads up to 10 API keys from your `.env`.
2. Cycles through them for each request.
3. If a key is rate-limited (HTTP 429), it skips to the next.
4. Keeps going until success or all keys are exhausted.

---

## 🧑‍🔬 Troubleshooting

- **401 Unauthorized:** Check your API keys and `.env` formatting.
- **Network/DNS errors:** Ensure your device or Replit has network access.
- **Slow responses:** Lower `CONTEXT_LIMIT` or run locally.
- **Model errors:** Print response content in `aria_llm.py` for debugging.
- **Memory too short/long:** Adjust `CONTEXT_LIMIT` in `.env`.
- **Rate-limited:** Use more keys or lower request frequency.

---

## 🔐 Security & Privacy

- **Keep API keys secret!** Never share or commit your `.env`.
- **Be mindful of PII:** All conversations go to OpenRouter’s servers.
- **Respect OpenRouter’s Terms of Service.**

---

## 🧪 Testing

- Mock API calls in tests.
- Simulate error codes (401, 429, 5xx) and ensure ARIA handles them.
- Test memory by feeding in fake chat histories.

---

## 🤝 Contributing

1. Fork the repo and create a feature branch.
2. Make your changes and add tests.
3. Open a pull request with details!
4. Keep code simple, explicit, and well-documented.

---

## 🛣️ Roadmap

- Voice (TTS/STT) integration.
- Web/file/tool plugins.
- Streaming, partial outputs.
- Persistent storage (SQLite, vector DB).
- Key rotation/admin UI.

---

## 📄 License

_No license yet!_  
Suggest: MIT (permissive), Apache-2.0, or GPL-3.0.  
Add a `LICENSE` file to specify.

---

## ✨ One-Line Summary

ARIA: async, memory-enabled, personality-driven conversational AI using OpenRouter models — with API key rotation and long-term memory.
 
