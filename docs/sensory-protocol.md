# Sensory Protocol — Expanded Notes

## Why the hierarchy exists

Pixel data is high-bandwidth and expensive for local vision models. A 10-minute 1080p video at even 1 fps already produces 600 frames. Most of those frames are redundant. The 5-Senses protocol forces the agent to extract the maximum information from text first, then sample only the frames that actually resolve remaining uncertainty.

Empirical observation (mirrored in production systems such as Gemini): transcript + metadata frequently answers 60–80 % of user questions about a video. Visual sampling is required mainly for:

- On-screen text / diagrams / charts
- Speaker identity / appearance
- Non-verbal actions and demonstrations
- Scene transitions that are not narrated

## Visual Debt

A *visual debt* is any statement in the transcript (or user question) that cannot be verified or understood without looking. Classic triggers:

- "as you can see here"
- "look at this graph / slide / diagram"
- "this is what the UI looks like"
- "watch what happens when I click…"
- User asks "what colour is the shirt / what is on the whiteboard"

Once debt is recorded, the agent must escalate through contact sheet before high-resolution frames.

## Contact Sheet Design

Recommended contact-sheet parameters (implemented by the host):

- 6 frames in a 2×3 or 3×2 grid
- Each thumbnail annotated with its absolute timestamp
- Range typically ±20–30 s around the debt timestamp
- Low resolution is acceptable (the point is scene confirmation, not OCR)

If the contact sheet still leaves ambiguity (tiny text, subtle motion), the agent may request exact-timestamp high-res frames and must justify the cost.

## Full-Video Mode

When the user explicitly requests a complete breakdown:

1. Build a transcript-derived timeline first.
2. Generate contact sheets at adaptive intervals:
   - < 5 min → every 30–60 s
   - 5–30 min → every 2–5 min
   - longer → chapter markers if available, else 5-min intervals
3. Synthesize section-by-section, clearly separating content before vs after any user-supplied "current time".

## Sensory Log (mandatory)

Every final answer ends with a log of the form:

```
--- Sensory Log ---
Touched : metadata (duration 12:34, title "…", channel "…")
Heard   : transcript 00:00–12:34 (or specific ranges)
Saw     : contact sheet 03:10–03:40 ; frames at 03:22, 03:28
Tasted  : cross-checked transcript against frames; no contradictions
```

This log is the primary accountability artifact and is what the optional Critic Harness scores against.
