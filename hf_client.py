import os, requests, time
from typing import Optional

class HuggingFaceClient:
    """Minimal client for Hugging Face Inference API (free)."""
    def __init__(self, token: Optional[str], model: str = "gpt2", timeout: int = 60):
        if not token:
            raise ValueError("Hugging Face API token required. Set HF_API_TOKEN in env.")
        self.token = token
        self.model = model
        self.timeout = timeout
        self.endpoint = f"https://api-inference.huggingface.co/models/{self.model}"
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def generate(self, prompt: str, max_length: int = 256, temperature: float = 0.7):
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_length,
                "temperature": temperature,
                "return_full_text": False
            }
        }
        resp = requests.post(self.endpoint, headers=self.headers, json=payload, timeout=self.timeout)
        if resp.status_code == 200:
            # Many generation models return [{'generated_text': '...'}] or {'error':...}
            try:
                data = resp.json()
                if isinstance(data, list) and "generated_text" in data[0]:
                    return data[0]["generated_text"]
                if isinstance(data, dict) and "generated_text" in data:
                    return data["generated_text"]
                # Some models return string directly
                if isinstance(data, str):
                    return data
                # Otherwise try to extract text fields
                if isinstance(data, list) and len(data)>0 and isinstance(data[0], dict):
                    # join text-like values
                    return " ".join(str(v) for v in data[0].values())
                return str(data)
            except Exception as e:
                return resp.text
        else:
            raise RuntimeError(f"Hugging Face API error {resp.status_code}: {resp.text}")
