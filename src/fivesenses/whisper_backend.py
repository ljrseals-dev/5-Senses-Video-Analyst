"""Hearing: local Whisper backend (faster-whisper). Fully offline once the model is cached."""
from __future__ import annotations
from typing import Protocol
from .types import Segment


class Transcriber(Protocol):
    def transcribe(self, audio_path: str) -> list[Segment]: ...


class FasterWhisperBackend:
    def __init__(self, model_size: str = "small", device: str = "auto",
                 compute_type: str = "auto", language: str | None = None):
        try:
            from faster_whisper import WhisperModel
        except ImportError as e:  # pragma: no cover
            raise RuntimeError("pip install 'fivesenses[whisper]'") from e
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        self.language = language

    def transcribe(self, audio_path: str) -> list[Segment]:
        segs, _info = self.model.transcribe(
            audio_path, language=self.language, vad_filter=True, beam_size=5)
        return [Segment(s.start, s.end, s.text.strip()) for s in segs if s.text.strip()]


def to_srt(segments: list[Segment]) -> str:
    def t(x):
        ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000)
        m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    return "\n".join(f"{i}\n{t(s.start)} --> {t(s.end)}\n{s.text}\n"
                     for i, s in enumerate(segments, 1))
