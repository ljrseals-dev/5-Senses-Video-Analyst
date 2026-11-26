"""Touch + acquire: metadata and audio via yt-dlp. Pass cookies.txt for bot walls.
Respect each site's terms and copyright; prefer openly licensed material for anything shared."""
from __future__ import annotations
import json, subprocess, os


def _base(cookies: str | None) -> list[str]:
    return ["yt-dlp"] + (["--cookies", cookies] if cookies else [])


def get_metadata(url: str, cookies: str | None = None) -> dict:
    out = subprocess.check_output(_base(cookies) + ["--dump-json", "--no-download", url])
    m = json.loads(out)
    return {k: m.get(k) for k in ("id", "title", "channel", "duration", "description",
                                  "view_count", "chapters", "webpage_url")}


def download_audio(url: str, out_dir: str, cookies: str | None = None) -> str:
    os.makedirs(out_dir, exist_ok=True)
    tmpl = os.path.join(out_dir, "%(id)s.%(ext)s")
    subprocess.check_call(_base(cookies) + ["-x", "--audio-format", "wav", "-o", tmpl, url])
    ids = [f for f in os.listdir(out_dir) if f.endswith(".wav")]
    return os.path.join(out_dir, sorted(ids)[-1])
