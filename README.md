# Intelligent-Customer-Support-Agent

# Intelligent Customer Support Agent (Hugging Face Inference API)

This project is a complete scaffold for an Intelligent Customer Support Agent using the free Hugging Face Inference API.
It includes:
- FastAPI backend (`main.py`) that proxies chat requests to Hugging Face and serves a simple web UI.
- `hf_client.py` — wrapper to call Hugging Face Inference API using an environment-stored token.
- Static single-page frontend (`static/index.html`, `static/app.js`, `static/style.css`) — simple chat UI.
- Dockerfile and `.devcontainer` for VS Code development.
- Example `.env.example` showing required environment variables.

## Quick start (local)
1. Clone or unzip this project.
2. Create a Hugging Face account and generate an access token (see: https://huggingface.co/docs/huggingface_hub/en/guides/inference). Save it.
3. Copy `.env.example` to `.env` and set `HF_API_TOKEN`.
4. Create a virtualenv and install requirements:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
5. Run the app:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
6. Open http://localhost:8000 in your browser.

## Notes
- This project uses the Hugging Face Inference API. Free usage is available with rate limits. See Hugging Face docs for limits and supported models.
- Pick a model that supports text generation or instruction-following. The default in `hf_client.py` is `gpt2` (small) for free demos — swap in any model id from the Hub.

## Files included
- main.py
- hf_client.py
- requirements.txt
- Dockerfile
- .env.example
- static/*
- .devcontainer/*
