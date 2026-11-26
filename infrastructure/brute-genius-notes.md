# Brute Genius — Exhaustive Search Layer

Repository: https://github.com/ljrseals-dev/redesigned-fiesta

Brute Genius is an MCP server that performs *exhaustive combinatorial search*. It is not a video tool; it is a prompt- and hyper-parameter optimisation engine that can be used to tune the 5-Senses sampling strategy for a particular local model.

## Typical Use Case

You want the optimal combination of:

- contact-sheet interval
- scene-change threshold
- maximum frames per short video
- transcript chunk size
- vision model temperature / context window settings

Define a discrete search space over those variables, supply a named objective (e.g. "accuracy on a 50-video validation set measured by a secondary judge model"), and let Brute Genius enumerate the full Cartesian product, score every combination, and return a ranked list.

## Safety

- Always call the planning tool first; it returns a cost ceiling.
- On paid backends the search can spend money rapidly.
- On a pure local Ollama + open-source judge setup the only cost is wall-clock compute.

## Integration Sketch

1. Export a validation set of (video, question, gold answer) triples.
2. Write a thin evaluation harness that runs the 5-Senses agent under a candidate parameter set and scores the result.
3. Register that harness as the objective function with Brute Genius.
4. Launch the search; consume the ranked results to hard-code the winning parameters into the production agent.

This is an offline, one-time (or periodic) optimisation step, not something that runs on every user query.
