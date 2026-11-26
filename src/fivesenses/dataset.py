"""Transcript -> Q&A JSONL for LoRA, with a Critic-Harness-style support filter (ALLOW/DENY)."""
from __future__ import annotations
import json, re
from .memory import chunk_segments
from .types import Segment

_W = lambda s: set(re.findall(r"[a-z0-9]{4,}", s.lower()))


def parse_qa(text: str) -> list[tuple[str, str]]:
    return [(q.strip(), a.strip()) for q, a in
            re.findall(r"Q:\s*(.+?)\s*\nA:\s*(.+?)(?=\nQ:|\Z)", text, re.S)]


def supported(answer: str, source: str, min_overlap: float = 0.6) -> bool:
    """DENY answers whose content words are mostly absent from the source chunk."""
    aw = _W(answer)
    return bool(aw) and len(aw & _W(source)) / len(aw) >= min_overlap


def build_dataset(segs: list[Segment], llm, out_path: str, title: str = "", max_chars: int = 1500) -> dict:
    kept = dropped = 0
    with open(out_path, "a", encoding="utf-8") as f:
        for c in chunk_segments(segs, max_chars):
            raw = llm.chat([{"role": "system", "content": "From the transcript write 3 Q&A pairs. Format exactly 'Q: ...\\nA: ...'. Answers must use only facts in the transcript."},
                            {"role": "user", "content": c["text"]}])
            for q, a in parse_qa(raw):
                if supported(a, c["text"]):
                    f.write(json.dumps({"messages": [
                        {"role": "user", "content": q}, {"role": "assistant", "content": a}],
                        "source": title, "start": c["start"]}) + "\n"); kept += 1
                else:
                    dropped += 1
    return {"kept": kept, "dropped": dropped}
