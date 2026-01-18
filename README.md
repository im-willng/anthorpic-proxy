# anthropic-proxy

Anthropic-compatible proxy that allows you to run **Anthropic SDK, Claude Code, and Claude-compatible tools** on **multiple LLMs** (GPT, Gemini, etc.) and **multiple providers** such as **Ollama, Vertex AI, and Bedrock** — without changing client code.

The project is implemented using **FastAPI** and acts as a unified compatibility layer between Anthropic-style requests and various LLM backends.

---

## Features

* ✅ Anthropic API–compatible endpoints
* 🔁 Route Claude-style requests to non-Claude models (GPT, Gemini, LLaMA, ...)
* 🔌 Support for multiple providers (Ollama, Vertex AI, Bedrock, OpenAI, ...)
* 🔐 Keep provider API keys on the server side
* 🧩 Extensible architecture (adapters / providers)
* 🚀 Drop-in replacement for Anthropic API in existing tools

---

## Requirements

* Python **3.9+** (recommended 3.10 or 3.11)
* pip or poetry

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-org/anthropic-proxy.git
cd anthropic-proxy
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux / macOS
# .venv\\Scripts\\activate  # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Server

### Development

Run FastAPI with auto-reload:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8082 --reload
```

---

## API Usage

Once running, the proxy exposes **Anthropic-compatible endpoints**.

Example base URL:

```
http://localhost:8082
```

### Example: Using Anthropic SDK

Configure your client to point to the proxy instead of Anthropic:

```bash
export ANTHROPIC_BASE_URL=http://localhost:8082
export ANTHROPIC_API_KEY=dummy-key
```

Your existing Anthropic / Claude code should work without modification.

---

## Provider Routing (Concept)

Requests received in Anthropic format are:

1. Validated against the Anthropic API schema
2. Mapped to an internal request format
3. Routed to the selected provider + model
4. Translated back into an Anthropic-compatible response

Provider / model selection may be based on:

* Environment defaults
* Request metadata
* Custom routing logic

---


## Use Cases

* Run **Claude Code** on GPT / Gemini
* Avoid vendor lock-in
* Centralize LLM access across teams
* Self-hosted or on-prem LLM routing
* Experiment with multiple models behind a stable API