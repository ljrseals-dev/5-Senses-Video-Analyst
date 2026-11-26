# Learning from Videos — Beyond the 5-Senses Scaffold

**Important:** The 5-Senses package is an **inference-time scaffold**.  
It improves how a model *reads* a single video at run time. It does **not** change any model weights.  
True “learning” from YouTube, PBS, sports matches, or any other video corpus is a separate, heavier job.

There are three practical ways to do it, ordered from lightest to heaviest.

---

## 1. Retrieval Memory (no training — start here)

For each video:

1. Download with `yt-dlp` (respect cookies / terms).
2. Transcribe with Whisper (prefer the audio track over platform auto-captions).
3. Extract scene-change frames (vidlizer, claude-real-video, or ffmpeg + scene detection).
4. Ask a strong local model to write **timestamped notes** from the transcript + key frames.
5. Store the notes (and optionally the transcript chunks) in a vector database.
6. At query time, retrieve the relevant notes and inject them into the 5-Senses context.

The model now has access to everything it has previously “watched,” with zero GPU training.  
For PBS / educational content this routinely delivers ~90 % of the practical value, and you can add a new video at any time.

**Fits cleanly under the 5-Senses protocol:** the retrieved notes become an extra “Touch / Smell” source that the agent can cite in its Sensory Log.

---

## 2. Fine-tuning on Text from the Videos (LoRA / QLoRA)

Turn transcripts into supervised training data:

1. Chunk each transcript by topic (chapter markers or sentence boundaries).
2. Have a strong local model generate Q&A pairs, summaries, and explanations from each chunk.
3. **Filter aggressively.** The Critic Harness idea fits perfectly here: keep only pairs whose answer is supported by the source transcript.
4. Fine-tune with LoRA or QLoRA (Unsloth, Axolotl, LLaMA-Factory, etc.) on a base such as Qwen or Llama.

This teaches the model facts and style.  
It works best **together with** the retrieval memory above; fine-tuning alone tends to blur or invent details.

---

## 3. True Video-Language Training (research-grade)

Fine-tune a vision-language model (Qwen-VL, SmolVLM2, …) on `(frames, transcript, instruction)` tuples so the model learns to connect visuals with speech.

- Requires large amounts of paired data, significant GPU time, and careful evaluation.
- Do **not** start here.

---

## Rights and Quality Cautions

- YouTube and PBS content is copyrighted. Downloading for training is often restricted by terms of service.  
  Personal-use retrieval or private fine-tuning is lower risk than redistributing a model or dataset.  
  For anything you intend to share, prefer openly licensed material (CC-BY lectures, Khan Academy-style content that permits reuse, etc.).
- Auto-captions contain errors. Always prefer Whisper (or better) run on the actual audio track, and compare before training.
- “Match videos” (sports): text alone loses most of the signal. Learning rules, tactics, player tracking, or score events requires the third path (or specialised event-detection models).

---

## Recommended Order of Work

1. Wire the 5-Senses tools to vidlizer or claude-real-video and get **one** video answered well.
2. Add the notes-plus-vector-store memory layer and ingest a small PBS / educational playlist.
3. Build a transcript → Q&A dataset, then run a small LoRA on a 3–8 B model.
4. Evaluate on held-out videos. Only then consider full video-language training.

---

## Next Steps This Repo Can Support

- Ingestion script outline: `yt-dlp → Whisper → scene frames → notes → vector store`
- Transcript-to-Q&A generator that uses the Critic Harness filtering idea
- Evaluation harness that scores 5-Senses answers against gold notes

Ask for any of these and they can be added as concrete scripts or further documentation.
