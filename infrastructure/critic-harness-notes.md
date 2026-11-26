# Critic Harness — Accountability Layer

The 5-Senses protocol produces claims that must be grounded. The Critic Harness (reference implementation associated with the ljrseals-dev classical AI laboratory) supplies a runtime gate that adjudicates those claims.

## Integration Pattern

1. The Five-Senses agent emits a candidate answer + Sensory Log.
2. The Critic Harness receives the answer, the log, and the raw tool results that were used.
3. Each factual assertion is scored against an evidence baseline:
   - Does the claim cite a sense that was actually invoked?
   - Does the cited sense contain supporting data?
   - Is the claim stronger than the evidence warrants?
4. Harness returns one of:
   - `ALLOW` — claim is fully supported
   - `CONDITIONAL` — claim is plausible but requires hedging language
   - `DENY` — claim is unsupported or contradicted
   - `ESCALATE` — more sensory data required before a decision

## Practical Effect

- "The speaker is angry" is denied unless the transcript contains affective language *or* a visual frame shows clear facial expression that was sampled.
- "The chart shows a 40 % increase" is allowed only if the contact sheet or high-res frame was inspected and the number is visible (or the transcript explicitly states the number).
- Pure title-based guesses are forced into the "Assumption from Touch" labelling required by the Output Contract.

## Where to Find the Reference

Look for Critic Harness / Artifact Harness / Cyclinic Model implementations under the ljrseals-dev organisation, particularly repositories tagged with the 5-Senses classical AI laboratory (METHODS, 5-Senses-LeWM, etc.). The harness is language-model agnostic and can sit in front of any Ollama or OpenAI-compatible endpoint.
