import json, urllib.parse
from fivesenses.types import Segment
from fivesenses.memory import Memory
from fivesenses import agent
from fivesenses.dataset import build_dataset, parse_qa, supported
from fivesenses.elevenlabs_tts import ElevenLabsTTS
from fivesenses.whisper_backend import to_srt


class FakeSTT:
    def transcribe(self, p):
        return [Segment(0, 5, "Photosynthesis converts sunlight into chemical energy in chloroplasts."),
                Segment(5, 10, "Chlorophyll absorbs mostly red and blue light.")]


class FakeLLM:
    def __init__(self): self.calls = []
    def chat(self, m, temperature=0.2):
        self.calls.append(m)
        if "Q&A" in m[0]["content"]:
            return ("Q: What absorbs light?\nA: Chlorophyll absorbs red and blue light.\n"
                    "Q: Who won?\nA: Napoleon conquered Antarctica quickly.")
        return "ok"


def test_ingest_and_ask(tmp_path):
    mem, llm = Memory(str(tmp_path / "m.db")), FakeLLM()
    assert agent.ingest("u", {"id": "v1", "title": "Bio", "duration": 10}, "x.wav", FakeSTT(), llm, mem) == 1
    assert agent.ask("what absorbs light chlorophyll", llm, mem) == "ok"
    assert "Chlorophyll" in llm.calls[-1][1]["content"] and "Five-Senses" in llm.calls[-1][0]["content"]


def test_dataset_filters_unsupported(tmp_path):
    out = tmp_path / "qa.jsonl"
    stats = build_dataset(FakeSTT().transcribe(""), FakeLLM(), str(out), "Bio")
    assert stats == {"kept": 1, "dropped": 1}
    assert json.loads(out.read_text())["messages"][1]["content"].startswith("Chlorophyll")


def test_tts_request():
    r = ElevenLabsTTS("VOICE", api_key="k").build_request("hi")
    assert r.full_url.startswith("https://api.elevenlabs.io/v1/text-to-speech/VOICE")
    assert r.headers["Xi-api-key"] == "k" and json.loads(r.data)["text"] == "hi"


def test_srt():
    assert "00:00:00,000 --> 00:00:05,000" in to_srt(FakeSTT().transcribe(""))
