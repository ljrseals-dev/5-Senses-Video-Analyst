from __future__ import annotations
from dataclasses import dataclass, asdict


@dataclass
class Segment:
    start: float
    end: float
    text: str

    def to_dict(self):
        return asdict(self)


def fmt_ts(sec: float) -> str:
    sec = int(sec)
    h, r = divmod(sec, 3600)
    m, s = divmod(r, 60)
    return f"{h:d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
