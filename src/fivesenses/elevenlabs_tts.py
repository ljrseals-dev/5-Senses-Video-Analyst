"""Voice: ElevenLabs text-to-speech over REST (stdlib only). Needs ELEVENLABS_API_KEY."""
from __future__ import annotations
import json, os, urllib.request

API = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"


class ElevenLabsTTS:
    def __init__(self, voice_id: str | None = None, model_id: str = "eleven_multilingual_v2",
                 api_key: str | None = None, output_format: str = "mp3_44100_128"):
        self.api_key = api_key or os.environ.get("ELEVENLABS_API_KEY")
        self.voice_id = voice_id or os.environ.get("ELEVENLABS_VOICE_ID")
        if not self.api_key:
            raise RuntimeError("Set ELEVENLABS_API_KEY")
        if not self.voice_id:
            raise RuntimeError("Set ELEVENLABS_VOICE_ID or pass voice_id")
        self.model_id, self.output_format = model_id, output_format

    def build_request(self, text: str) -> urllib.request.Request:
        url = API.format(voice_id=self.voice_id) + f"?output_format={self.output_format}"
        body = json.dumps({"text": text, "model_id": self.model_id}).encode()
        return urllib.request.Request(url, data=body, method="POST", headers={
            "xi-api-key": self.api_key, "Content-Type": "application/json",
            "Accept": "audio/mpeg"})

    def speak(self, text: str, out_path: str) -> str:
        with urllib.request.urlopen(self.build_request(text), timeout=120) as r, open(out_path, "wb") as f:
            f.write(r.read())
        return out_path
