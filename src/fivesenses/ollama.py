"""Reasoning: minimal Ollama client (stdlib)."""
from __future__ import annotations
import json, os, urllib.request

HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")


class Ollama:
    def __init__(self, model: str = "qwen2.5vl:3b", host: str = HOST):
        self.model, self.host = model, host.rstrip("/")

    def chat(self, messages: list[dict], temperature: float = 0.2) -> str:
        body = json.dumps({"model": self.model, "messages": messages, "stream": False,
                           "options": {"temperature": temperature}}).encode()
        req = urllib.request.Request(self.host + "/api/chat", data=body,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=600) as r:
            return json.loads(r.read())["message"]["content"]
