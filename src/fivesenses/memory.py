"""Smell/long-term memory: SQLite FTS5 store of timestamped transcript chunks + notes."""
from __future__ import annotations
import re, sqlite3
from .types import Segment, fmt_ts


def chunk_segments(segs: list[Segment], max_chars: int = 1200) -> list[dict]:
    chunks, cur = [], []
    def flush():
        if cur:
            chunks.append({"start": cur[0].start, "end": cur[-1].end,
                           "text": " ".join(s.text for s in cur)})
    size = 0
    for s in segs:
        if size + len(s.text) > max_chars and cur:
            flush(); cur.clear(); size = 0
        cur.append(s); size += len(s.text) + 1
    flush()
    return chunks


class Memory:
    def __init__(self, path: str = "fivesenses.db"):
        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS videos(id TEXT PRIMARY KEY, title TEXT, url TEXT, duration REAL)")
        self.db.execute("CREATE VIRTUAL TABLE IF NOT EXISTS chunks USING fts5(video_id UNINDEXED, start UNINDEXED, end UNINDEXED, kind UNINDEXED, text)")

    def add_video(self, vid: str, title: str, url: str, duration: float | None, chunks: list[dict], notes: str = ""):
        self.db.execute("INSERT OR REPLACE INTO videos VALUES(?,?,?,?)", (vid, title, url, duration))
        self.db.execute("DELETE FROM chunks WHERE video_id=?", (vid,))
        for c in chunks:
            self.db.execute("INSERT INTO chunks VALUES(?,?,?,?,?)", (vid, c["start"], c["end"], "transcript", c["text"]))
        if notes:
            self.db.execute("INSERT INTO chunks VALUES(?,?,?,?,?)", (vid, 0, duration or 0, "notes", notes))
        self.db.commit()

    def search(self, query: str, k: int = 5) -> list[dict]:
        terms = re.findall(r"\w+", query)
        if not terms:
            return []
        q = " OR ".join(f'"{t}"' for t in terms)
        rows = self.db.execute(
            "SELECT c.video_id, v.title, c.start, c.end, c.kind, c.text FROM chunks c "
            "JOIN videos v ON v.id=c.video_id WHERE chunks MATCH ? ORDER BY rank LIMIT ?", (q, k)).fetchall()
        return [dict(zip(("video_id", "title", "start", "end", "kind", "text"), r)) for r in rows]


def format_hits(hits: list[dict]) -> str:
    return "\n\n".join(f"[{h['title']} {fmt_ts(float(h['start']))}-{fmt_ts(float(h['end']))} ({h['kind']})]\n{h['text']}" for h in hits)
