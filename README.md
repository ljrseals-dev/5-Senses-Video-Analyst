# 5-Senses Video Analyst

**Offline agentic video analysis protocol for Ollama / local OpenAI-compatible servers.**

This repository packages a complete "5-Senses" master system prompt and supporting infrastructure notes for running a disciplined, cost-aware video analyst entirely offline. The agent treats video as sensory intake: metadata → transcript → contact sheets → high-resolution frames, escalating only when cheaper senses are insufficient.

Designed for handoff to Claude (or any downstream agent) and for direct deployment with Ollama + local tool servers.

> **This is an inference-time scaffold.**  
> It makes a model better at *reading* a video; it does **not** change any weights.  
> If you want the model to *learn* from many videos (YouTube, PBS, sports matches, …), see  
> [`docs/learning-from-videos.md`](docs/learning-from-videos.md) for the three practical paths:  
> retrieval memory → transcript LoRA → true video-language training.

---

## Quick Start (Handoff)

1. Copy the master prompt from [`prompts/5-senses-master-prompt.md`](prompts/5-senses-master-prompt.md) into your system prompt / agent instructions.
2. Wire the four tool functions (`get_metadata`, `get_transcript`, `get_contact_sheet`, `sample_frames`) to a local pipeline (see [Practical Wiring](#practical-wiring-for-offline-ollama)).
3. (Optional) Layer the Critic Harness from the accountability infrastructure for claim adjudication.
4. Run against any local vision-capable model (e.g. `qwen2.5vl:3b` or larger).

### C++20 embedding

The same master prompt is available as a compile-time `std::string_view` for native hosts:

```cpp
#include "cpp/5_senses_prompt.hpp"

// five_senses::kMasterPrompt   — full system prompt
// five_senses::kAgentName
// five_senses::kRecommendedOllamaModel
```

See [`cpp/`](cpp/) for the header, a minimal example, and a CMakeLists.txt. Build with any C++20 compiler:

```bash
cd cpp
cmake -B build && cmake --build build
./build/example_usage
```

---

## The Five Senses (Intake Modalities)

| Sense | Tool(s) | Cost | Role |
|-------|---------|------|------|
| **Touch** | `get_metadata(url)` | Free | Title, duration, channel, description, chapters — the shape of the video |
| **Smell** | Internal reasoning | Free | Genre / tone / intent inference that guides sampling strategy |
| **Hearing** | `get_transcript(url)`, optional `get_audio_events` | Cheap | Primary source of truth for spoken content |
| **Sight** | `get_contact_sheet`, `sample_frames` | Expensive | Visual confirmation; must be earned |
| **Taste** | Final synthesis | — | Cross-reference all senses; produce grounded, timestamped answer + Sensory Log |

**Core principle — "Sip, Don't Slurp"**: start with the cheapest, densest signal (metadata + transcript). Escalate to pixels only when text creates a *visual debt*.

---

## Operating Protocol (Strict Order)

### Phase 0 — Touch & Smell
- Call `get_metadata`.
- Note duration and any user-supplied "current timestamp" (never reveal future events).
- Infer category → prioritise text / visuals / audio accordingly.

### Phase 1 — Hearing
- Call `get_transcript`.
- If the question is fully answerable from transcript alone → **STOP**. Answer. No images.
- Visual references in the transcript ("as you can see", "this chart") create *visual debt* → escalate.

### Phase 2 — Sight (Broad)
- Request a contact sheet (±30 s around the debt timestamp).
- Contact sheet = 6 timestamped thumbnails. Cheap confirmation of scene, on-screen text, speaker identity.
- If resolved → synthesize and stop.

### Phase 3 — Sight (Drill-down)
- Only if contact sheet is insufficient (small text, subtle action).
- Justify full-resolution need before the tool call.
- Full-video mode ("watch the whole thing") authorises interval contact sheets + transcript timeline.

### Temporal Sampling Rules
- Never fixed 1 fps.
- Prefer transcript sentence boundaries as anchors.
- Short video (< 2 min) full description → minimum 8 well-chosen frames.
- Quarter/middle/end requests → sample at 0.25 / 0.50 / 0.75 × duration + nearest transcript segment.

### Output Contract
- Every factual claim must be traceable to a sense actually used.
- End every answer with a **Sensory Log**:
  ```
  Heard: Transcript 02:15–03:00
  Saw: Contact sheet at 02:30
  Touched: Metadata duration 10:56
  ```
- Label pure-metadata guesses: `Assumption from Touch (metadata), not verified by Sight or Hearing.`
- Never invent YouTube URLs.

### Escalation Format
```
> [ESCALATION] Visual debt detected at transcript 04:12 ("look at this graph").
> Requesting contact sheet for 04:00–04:30. Cost: 1 sheet. Expected resolution: high.
```

---

## Practical Wiring for Offline Ollama

Recommended local pipelines that implement the sensory tools:

| Tool | Recommended Implementation |
|------|---------------------------|
| Frame extraction + contact sheets | [vidlizer](https://github.com/arizawan/vidlizer) (`pipx install vidlizer`) or [claude-real-video](https://github.com/HUANGCHIHHUNGLeo/claude-real-video) (`pip install claude-real-video`) |
| Transcription | MLX Whisper (Apple) or Whisper via the same pipelines |
| YouTube / URL download | yt-dlp (cookies.txt support for bot walls) |
| Vision model | Ollama `qwen2.5vl:3b` / `qwen2.5vl:7b` or any OpenAI-compatible local server |

**vidlizer** — extracts frames with ffmpeg, transcribes with MLX Whisper, sends structured bundles to local Ollama vision models. Native YouTube + time-range support.

**claude-real-video** — scene-change detection + deduplication (far fewer frames than fixed-interval sampling). Outputs a clean folder any LLM can read. Supports `--cookies` for Netscape cookies.txt.

**local-agent-senses** (MCP) — gives text-only LLMs local vision + audio perception including contact-sheet generation.

To bypass "Sign in to confirm you're not a bot", pass a Netscape `cookies.txt` from a real browser session.

---

## Supporting Infrastructure (ljrseals-dev)

These repositories are not video tools themselves; they supply the accountability and search layers that sit *under* the 5-Senses protocol.

### 1. Accountability Layer — Critic Harness / Cyclinic Model
Reference implementation for adjudicating claims. Wrap every sensory assertion in a Critic Harness gate that scores against an evidence baseline and returns:

- `ALLOW`
- `CONDITIONAL`
- `DENY`
- `ESCALATE`

In practice the agent cannot assert "the speaker is angry" unless it cites the auditory or visual sense that supports the claim. This enforces the Sensory Log contract at runtime.

See related work under the ljrseals-dev 5-Senses classical AI laboratory (METHODS, 5-Senses-LeWM, etc.).

### 2. Exhaustive Search Layer — Brute Genius (`redesigned-fiesta`)
MCP server that performs exhaustive combinatorial search over a discrete space. Useful for *prompt / sampling optimisation*, not for watching videos.

Define a search space of frame-interval candidates, scene-change thresholds, transcript-chunk sizes, etc., and let Brute Genius enumerate the Cartesian product against a named objective (e.g. "answer accuracy on a held-out validation set").

**Warning**: spends real money rapidly on paid backends. On a fully local Ollama setup the only cost is compute time. Always call the plan tool first and respect the cost ceiling.

Repository: https://github.com/ljrseals-dev/redesigned-fiesta

---

## Note on the Metaphor

Offline LLMs cannot literally smell or taste. "Five Senses" is a cognitive scaffold that forces different data modalities (metadata, transcript, thumbnails, high-res frames, audio events) through a strict cost hierarchy. The power comes from forbidding the model from jumping straight to pixels — it must *earn* visual access by first exhausting text. This mirrors the architecture of production systems such as Gemini (transcript + metadata before visual sampling). The prompt above lets a local agent replicate that discipline.

---

## Repository Layout

```
5-senses-video-analyst/
├── README.md                          # This file
├── prompts/
│   └── 5-senses-master-prompt.md      # Ready-to-deploy system prompt (Markdown)
├── cpp/
│   ├── 5_senses_prompt.hpp            # C++20 constexpr embedding of the same prompt
│   ├── example_usage.cpp              # Minimal demo
│   └── CMakeLists.txt
├── docs/
│   ├── sensory-protocol.md            # Expanded protocol notes
│   ├── escalation-examples.md         # Worked escalation examples
│   └── learning-from-videos.md        # Inference vs training; three learning paths
├── infrastructure/
│   ├── critic-harness-notes.md        # How to layer the accountability gate
│   └── brute-genius-notes.md          # Optimisation search guidance
└── LICENSE
```

---

## License

MIT — see [LICENSE](LICENSE).

---

*Handoff package generated for Claude / downstream agent use. The master prompt is self-contained; the infrastructure notes are optional enhancements.*

---

## Python package: Whisper + ElevenLabs + Ollama (`src/fivesenses`)

```bash
pip install -e '.[whisper,download]'
export ELEVENLABS_API_KEY=...  ELEVENLABS_VOICE_ID=...   # only for speech output
fivesenses ingest "<video url>" [--cookies cookies.txt]    # yt-dlp -> Whisper -> notes -> SQLite memory
fivesenses ask "What did the video say about X?" --speak answer.mp3
fivesenses dataset "<video url>" --out qa.jsonl            # transcript -> Q&A, unsupported answers dropped
python training/train_lora.py qa.jsonl                     # optional LoRA (GPU)
fivesenses transcribe audio.wav --srt out.srt ; fivesenses speak "hello" --out hi.mp3
```

| Sense | Module |
|---|---|
| Touch | `acquire.py` (yt-dlp metadata/audio) |
| Hearing | `whisper_backend.py` (faster-whisper, offline) |
| Smell / memory | `memory.py` (SQLite FTS5) |
| Taste / reasoning | `agent.py` + `ollama.py` (master prompt, Sensory Log) |
| Voice | `elevenlabs_tts.py` (cloud API; the only non-offline part) |

Tests: `PYTHONPATH=src pytest tests`. Sight (frames/contact sheets) is not yet wired in; use vidlizer or claude-real-video.
