"""Ingest videos into memory, and answer questions grounded in what was heard."""
from __future__ import annotations
import os
from .memory import Memory, chunk_segments, format_hits
from .types import fmt_ts

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "master_prompt.md")


def master_prompt() -> str:
    with open(PROMPT_PATH, encoding="utf-8") as f:
        return f.read()


def ingest(url, meta: dict, audio_path: str, stt, llm, mem: Memory, make_notes: bool = True):
    segs = stt.transcribe(audio_path)
    chunks = chunk_segments(segs)
    notes = ""
    if make_notes and segs:
        tx = "\n".join(f"[{fmt_ts(s.start)}] {s.text}" for s in segs)[:24000]
        notes = llm.chat([{"role": "system", "content": "Write concise timestamped study notes. Use only the transcript."},
                          {"role": "user", "content": tx}])
    mem.add_video(meta.get("id") or url, meta.get("title") or url, url, meta.get("duration"), chunks, notes)
    return len(chunks)


def ask(question: str, llm, mem: Memory, k: int = 5) -> str:
    hits = mem.search(question, k)
    ctx = format_hits(hits) or "(no matching memory)"
    return llm.chat([{"role": "system", "content": master_prompt()},
                     {"role": "user", "content": f"MEMORY (Hearing):\n{ctx}\n\nQUESTION: {question}\nEnd with a Sensory Log."}])
