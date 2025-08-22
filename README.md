# ARIA: Artificial Realistic Intelligence Agent

ARIA (Artificial Realistic Intelligence Agent) is an advanced Python-based framework for building intelligent, realistic, and adaptable AI agents. It features modular architecture, persistent memory, dynamic personality settings, and seamless integration with modern LLM APIs (such as OpenRouter).

---

## 🚀 Features

- **LLM Integration** — Interact with state-of-the-art Large Language Models
- **Persistent Memory** — Uses LangChain for ongoing, context-rich conversations
- **Customizable Personality** — Easily define and swap agent personas
- **API Key Management** — Automatic rotation and secure storage
- **Modular Design** — Clean codebase for easy extension and maintenance

---

## 📦 Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/Dinos17/ARIA-Artificial_Realistic_Intelligence_Agent.git
    cd ARIA-Artificial_Realistic_Intelligence_Agent
    ```

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    > _If `requirements.txt` is missing, install packages based on code imports._

3. **Configure environment variables**
    - Create a `.env` file in the root directory.
    - Add your API keys and other configuration settings as needed.

---

## 🛠️ Usage

Start ARIA from the command line:
```bash
python main.py
```
You can modify `main.py` or extend the framework to fit your interface and use case.

---

## 🗂️ Project Structure

- `main.py` — Main entry point
- `aria_llm.py` — Core LLM interaction logic
- `personality_aria.py` — Personality configuration and switching
- `langchain_memory.py` — Conversational memory integration
- `key_rotation_openrouter.py` — API key management
- `.env` — (Not tracked) Environment-specific configuration

---

## 🧩 Customization

- **Create new personalities**: Edit or add to `personality_aria.py`
- **Swap LLMs/providers**: Update `aria_llm.py` and your `.env` file
- **Extend memory**: Modify `langchain_memory.py` for different persistence strategies

---

## 🤝 Contributing

Contributions and suggestions are welcome!
- Fork the repo and submit pull requests
- Open issues for bugs or feature requests

---

## 📄 License

_No license file detected. Please add a LICENSE file if you intend to open source this project._

---

**Author:** [Dinos17](https://github.com/Dinos17)- **Main Entry Point:** `main.py` provides the CLI or app interface for running ARIA.

## Getting Started

### Prerequisites

- Python 3.8+
- Access to OpenRouter or another supported LLM API
- Required Python packages (see code for details)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Dinos17/ARIA-Artificial_Realistic_Intelligence_Agent.git
   cd ARIA-Artificial_Realistic_Intelligence_Agent
   ```

2. **Set up environment variables:**
   - Copy the `.env` template or create your own with appropriate API keys and settings.

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(If `requirements.txt` is not present, review imports in the Python files and install necessary packages.)*

### Running ARIA

```bash
python main.py
```

Modify or extend `main.py` to suit your interface needs.

## File Overview

- `aria_llm.py`: Core logic for LLM interactions.
- `langchain_memory.py`: Integrates LangChain memory with ARIA.
- `personality_aria.py`: Defines ARIA's personality traits and behaviors.
- `key_rotation_openrouter.py`: Handles API key rotation for OpenRouter.
- `.env`: (Sensitive) Environment variables for API access and configuration.
- `main.py`: Project entry point.

## Customization

- **Personalities:** Edit or extend `personality_aria.py` to build new agent personas.
- **Memory:** Adjust memory logic in `langchain_memory.py` for custom persistence.
- **LLM Providers:** Update `aria_llm.py` and `.env` for new models or providers.

## License

*No license file detected. Please add a LICENSE file for open source compliance.*

## Contributing

Contributions, issues, and feature requests are welcome! Please use issues and pull requests via [GitHub](https://github.com/Dinos17/ARIA-Artificial_Realistic_Intelligence_Agent).

---

**Author:** [Dinos17](https://github.com/Dinos17)
````
