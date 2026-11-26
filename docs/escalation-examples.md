# Escalation Examples

## Example 1 — Transcript alone is sufficient

**User**: "What does the speaker say about the quarterly numbers?"

**Agent behaviour**:
1. `get_metadata` → duration 08:12, title contains "Q3 earnings"
2. `get_transcript` → finds the relevant segment at 04:18–05:02
3. Answer from transcript only. No escalation.

**Sensory Log**:
```
Touched: metadata duration 08:12
Heard: transcript 04:18–05:02
Saw: none
```

---

## Example 2 — Visual debt resolved by contact sheet

**User**: "What does the chart at the 3-minute mark show?"

**Agent behaviour**:
1. Metadata + transcript confirm a chart is referenced around 03:05 ("as you can see on this chart…")
2. Escalation:

> [ESCALATION] Visual debt at transcript 03:05 ("as you can see on this chart"). Requesting contact sheet 02:50–03:20. Cost: 1 sheet. Expected resolution: high.

3. Contact sheet shows a bar chart with labelled axes. Agent reads the visible numbers and answers.
4. No high-res frames needed.

**Sensory Log**:
```
Touched: metadata
Heard: transcript 02:50–03:20
Saw: contact sheet 02:50–03:20
```

---

## Example 3 — Contact sheet insufficient → high-res frames

**User**: "Can you read the fine print on the slide at 07:40?"

**Agent behaviour**:
1. Transcript confirms a slide is shown.
2. Contact sheet requested → text is present but illegible at thumbnail resolution.
3. Second escalation:

> [ESCALATION] Contact sheet confirms slide is visible but text is too small. Requesting high-resolution frame at 07:42. Cost: 1 frame. Justification: OCR of fine print required by user question.

4. Frame returned, text transcribed, answer given.

---

## Example 4 — Full-video request with current timestamp

**User**: "I've watched up to 04:30. Give me a complete breakdown of the whole video so far and a preview of what remains."

**Agent behaviour**:
1. Metadata → duration 15:00
2. Transcript for entire video (or up to known end)
3. Contact sheets for 00:00–04:30 at 45 s intervals + one sheet for the remaining portion
4. Answer clearly partitions:

   **Completed (00:00–04:30)**  
   …  

   **Remaining (04:30–15:00)**  
   … (labelled as preview / not yet watched)

Never treat post-04:30 content as already observed by the user.
