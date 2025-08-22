# ARIA — Artificial Realistic Intelligence Agent

Calm, professional, and exactly as helpful as you ordered.

ARIA is a modular, async, LangChain-memory-enabled conversational assistant built around OpenRouter-hosted models (default: `qwen/qwen3-235b-a22b:free`). ARIA is designed to feel realistic by remembering long interactions via LangChain memory (buffer + summary), following a configurable personality module, and supporting robust API key rotation to avoid rate-limits. Lightweight enough for Replit; performant on a local PC.

---

## Features

- **Personalized personality module** (`personality_aria.py`): ARIA addresses you by name and simulates emotion-aware replies.
- **LangChain memory** (`langchain_memory.py`): Combines conversation buffer and automatic summarization for long-term memory without blowing tokens.
- **Async LLM wrapper** (`aria_llm.py`): Uses `httpx.AsyncClient`, handles retries, backoff, and status-code-aware errors.
- **Key rotation tool** (`key_rotation_openrouter.py`): Round-robin through multiple OpenRouter keys; automatically skips keys hitting rate limits (HTTP 429).
- **Modular main loop** (`main.py`): Interactive CLI, integrates memory and LLM, stores session memory in LangChain structures.
- **Config via `.env`**: Model selection, timeouts, retry limits, and multiple API keys are environment-driven.
- **Replit-compatible**: No forced venv usage required; works on local machine too.

---

## Architecture

```
User CLI <--> main.py
                 |
                 +--> langchain_memory.py  (ConversationBufferWindowMemory + ConversationSummaryMemory)
                 |
                 +--> aria_llm.py          (Async OpenRouter client; reads personality prompt)
                 |
                 +--> personality_aria.py  (System prompt template / personality rules)
                 |
                 +--> key_rotation_openrouter.py  (Optional standalone for bulk requests)
```

- `main.py` orchestrates: prompts user, requests context from ARIAMemory, calls ARIALLM, and updates memory.
- `langchain_memory.py` handles message buffering and summaries (LangChain memory objects).
- `aria_llm.py` is model agnostic — it reads `MODEL_ID` from environment; switching models only requires `.env` change.
- `personality_aria.py` is the single source of truth for ARIA’s tone and behavior.
- `key_rotation_openrouter.py` is a separate utility for batch workloads.

---

## File-by-file Description

### `.env`
Configuration for secrets and runtime settings. Example template:
```
OPENROUTER_API_KEY_1=sk-or-xxxxxxxxxxxxxxxxxxxxxx1
OPENROUTER_API_KEY_2=sk-or-xxxxxxxxxxxxxxxxxxxxxx2
...
OPENROUTER_API_KEY_10=sk-or-xxxxxxxxxxxxxxxxxxxxxx10

OPENROUTER_API_KEY=sk-or-...          # Optional single-key fallback
MODEL_ID=qwen/qwen3-235b-a22b:free    # Default model ID
CONTEXT_LIMIT=8                       # Recent turns to keep in buffer
REQUEST_TIMEOUT_SECONDS=60
MAX_RETRIES=3
```
- Use `OPENROUTER_API_KEY_N` for key rotation script.
- `OPENROUTER_API_KEY` is used by `aria_llm.py` if present (single-key mode).
- **Keep `.env` out of version control!**

---

### `personality_aria.py`
Defines ARIA’s voice, protocol, and example behaviors.
- **Function:** `get_personality_prompt(user_name: str = "User") -> str`
- Returns a system prompt that helps the LLM stay in-character.

---

### `langchain_memory.py`
Implements advanced LangChain memory pattern (buffer + summary).
- **Class:** `ARIAMemory(user_name: str, context_window: int = 8)`
- **Methods:** `load_history`, `get_context`, `update`, `dump_history`
- Uses `ConversationBufferWindowMemory` and `ConversationSummaryMemory`.

---

### `aria_llm.py`
Async API client for OpenRouter with robust retry/backoff and error handling.
- **Class:** `ARIALLM(api_key: Optional[str] = None, model_id: Optional[str] = None)`
- **Method:** `acomplete(user_input: str, chat_history: list, user_name: str) -> str`
- Handles 401/429/5xx with appropriate retries or errors.

---

### `main.py`
CLI interface orchestrating ARIA conversation.
- Asks for user name, maintains context, calls LLM, updates memory.
- Uses async loop, handles graceful shutdown.

---

### `key_rotation_openrouter.py`
Utility for batch requests across multiple API keys with automatic rotation on rate-limit.
- Loads keys, cycles with `itertools.cycle`, skips rate-limited keys.

---

## Installation & Setup

### Replit (recommended for quick test)
1. Create a new Repl (Python).
2. Add all project files.
3. In Replit "Secrets", add keys: `OPENROUTER_API_KEY_1`, ..., `OPENROUTER_API_KEY_10` (or `OPENROUTER_API_KEY` for single-key mode).
4. Set other `.env` keys as needed.
5. Install packages: `pip install httpx python-dotenv langchain`
6. Run `main.py`.

### Local Machine
1. Clone repo.
2. *(Optional)* Create venv:  
   `python3 -m venv venv && source venv/bin/activate`
3. Install dependencies:  
   `pip install httpx python-dotenv langchain`
4. Create `.env` file with your keys.
5. Run:  
   `python main.py`

---

## Usage Examples

**Start ARIA:**
```bash
python main.py
```
Sample session:
```
Hello! What is your name? Dino
ARIA online. Type 'exit' to shut me down, Dino.
Dino: hi ARIA
ARIA: Hello, Dino! How's your day going so far?
Dino: remind me about the meeting tomorrow
ARIA: Got it, Dino — when is the meeting scheduled?
...
```

**Run batch prompts with key rotation:**
```bash
python key_rotation_openrouter.py
```

---

## `.env` Template

```
# Primary single-key (optional)
OPENROUTER_API_KEY=sk-or-your-primary-key

# OR (for key rotation)
OPENROUTER_API_KEY_1=sk-or-key1
OPENROUTER_API_KEY_2=sk-or-key2
...
OPENROUTER_API_KEY_10=sk-or-key10

# Model and runtime
MODEL_ID=qwen/qwen3-235b-a22b:free
CONTEXT_LIMIT=8
REQUEST_TIMEOUT_SECONDS=60
MAX_RETRIES=3
```

---

## How Key Rotation Works

1. `key_rotation_openrouter.py` reads `OPENROUTER_API_KEY_1..10`.
2. Uses `itertools.cycle` to rotate keys.
3. Each prompt is attempted with current key.
4. On HTTP 429 (rate-limited), key is temporarily blocked and script proceeds to next.
5. Continues until success or all keys are exhausted.

*Note: Rotation can be integrated into `aria_llm.py` if desired.*

---

## Troubleshooting & Tips

- **401 Unauthorized:** Check key value, no stray quotes, verify on OpenRouter dashboard.
- **DNS errors:** Confirm outbound network access.
- **Slow responses:** Reduce `CONTEXT_LIMIT`, run locally, or enable streaming (advanced).
- **JSON decode errors:** Print response in `aria_llm.py` for diagnostics.
- **LangChain summarization:** Supply an LLM instance for automatic summary.
- **Rate-limiting:** Use key rotation for batch workloads.

---

## Security & Privacy

- **API keys are secrets.** Never commit `.env`; use Replit secrets or OS environment.
- **Personal data:** Model requests go to OpenRouter — do not send sensitive PII unless understood.
- **Rate-limits:** Respect OpenRouter terms of service.

---

## Testing

- Mock `httpx.AsyncClient.post` to simulate 200, 401, 429, and 5xx responses.
- Test `langchain_memory.py` by providing artificial histories; verify context/update logic.
- Test `key_rotation_openrouter.py` with invalid keys to ensure proper rotation.

---

## Contribution Guide

1. Fork the repo.
2. Create a feature branch: `git checkout -b feature/<name>`.
3. Install dependencies and run `main.py`.
4. Make changes; add tests for new behavior.
5. Open a PR with description and rationale.
6. Follow code style: simple, explicit, and documented.

---

## Roadmap / Next Enhancements

- Integrate text-to-speech and speech-to-text for full voice interactions.
- Add tooling (web search, file system, external APIs).
- Implement streaming output for partial results.
- Add persistent storage for long-term memory (SQLite/vector DB).
- Secure admin UI for key rotation and usage monitoring.

---

## License

*No license specified yet. Recommended: MIT (permissive), Apache-2.0, or GPL-3.0. Add a LICENSE file to clarify usage rights.*

---

## One-line Summary

ARIA — Artificial Realistic Intelligence Agent: async, LangChain-memory-enabled, personality-driven conversational assistant using OpenRouter Qwen3 models with support for API key rotation and long-term memory.
