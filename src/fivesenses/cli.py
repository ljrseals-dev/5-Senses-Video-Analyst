from __future__ import annotations
import argparse, json, sys
from .memory import Memory
from .ollama import Ollama


def main(argv=None):
    p = argparse.ArgumentParser("fivesenses")
    p.add_argument("--db", default="fivesenses.db"); p.add_argument("--model", default="qwen2.5vl:3b")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("ingest"); a.add_argument("url"); a.add_argument("--cookies"); a.add_argument("--whisper", default="small"); a.add_argument("--no-notes", action="store_true")
    b = sub.add_parser("ask"); b.add_argument("question"); b.add_argument("--speak", metavar="OUT.mp3"); b.add_argument("--voice")
    c = sub.add_parser("dataset"); c.add_argument("url"); c.add_argument("--out", default="qa.jsonl"); c.add_argument("--cookies"); c.add_argument("--whisper", default="small")
    t = sub.add_parser("transcribe"); t.add_argument("audio"); t.add_argument("--whisper", default="small"); t.add_argument("--srt")
    s = sub.add_parser("speak"); s.add_argument("text"); s.add_argument("--out", default="out.mp3"); s.add_argument("--voice")
    args = p.parse_args(argv)

    if args.cmd == "speak":
        from .elevenlabs_tts import ElevenLabsTTS
        print(ElevenLabsTTS(args.voice).speak(args.text, args.out)); return
    if args.cmd == "transcribe":
        from .whisper_backend import FasterWhisperBackend, to_srt
        segs = FasterWhisperBackend(args.whisper).transcribe(args.audio)
        out = to_srt(segs); open(args.srt, "w").write(out) if args.srt else print(out); return
    llm = Ollama(args.model); mem = Memory(args.db)
    if args.cmd == "ingest":
        from . import acquire, agent
        from .whisper_backend import FasterWhisperBackend
        meta = acquire.get_metadata(args.url, args.cookies)
        audio = acquire.download_audio(args.url, "audio", args.cookies)
        n = agent.ingest(args.url, meta, audio, FasterWhisperBackend(args.whisper), llm, mem, not args.no_notes)
        print(f"ingested {meta['title']!r}: {n} chunks")
    elif args.cmd == "ask":
        from . import agent
        ans = agent.ask(args.question, llm, mem); print(ans)
        if args.speak:
            from .elevenlabs_tts import ElevenLabsTTS
            ElevenLabsTTS(args.voice).speak(ans, args.speak)
    elif args.cmd == "dataset":
        from . import acquire
        from .dataset import build_dataset
        from .whisper_backend import FasterWhisperBackend
        meta = acquire.get_metadata(args.url, args.cookies)
        segs = FasterWhisperBackend(args.whisper).transcribe(acquire.download_audio(args.url, "audio", args.cookies))
        print(json.dumps(build_dataset(segs, llm, args.out, meta["title"])))


if __name__ == "__main__":
    main()
