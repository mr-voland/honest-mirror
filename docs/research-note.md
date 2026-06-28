# Research Note — The Honest Mirror

**Claim.** A neuro-symbolic agent can surface a person's sharpest value-contradiction *reproducibly and with a verifiable inference trail*, where a stateless LLM gives a different, unverifiable answer each time. We show this on a public-domain character with a ground-truth contradiction from literary criticism.

## 1. Problem

Ask an LLM "what is this person's core contradiction?" and you get a fluent sentence — different on every run, with no trail you can audit or correct. For an agent meant to *hold the thread* of who someone is, that is not enough: the self-model must persist, be inspectable, and reason under uncertainty. The Honest Mirror puts the discernment in a symbolic NAL layer (OmegaClaw's `|-`) and uses the LLM only for extraction.

## 2. Method — A/B with extraction held constant

Both branches start from the **same** input (`data/raskolnikov_source.md`). Atomisation is hand-verified and frozen, so the experiment isolates the *reasoning*, not the extraction.

- **Branch A — LLM end-to-end.** The reflection text → one prompt: "name the single core value-contradiction." Run ×3.
- **Branch B — Honest Mirror.** The frozen atoms → NAL pipeline on the engine: revision accumulates confidence; STATED vs ENACTED collide on one term → CONTESTED; abduction derives the hidden competing commitment; a gate classifies it; a receipt records premises → rule → truth-value → gate. Run ×2.

**Ground truth** (`data/raskolnikov_ground_truth.md`): Raskolnikov's "extraordinary man / право имею" theory (the right to transgress morality for an idea) collides with his own conscience-bound, compassionate nature — the theory is refuted by himself.

Reproduce: `python3 bench/run_ab.py` inside the OmegaClaw container.

## 3. Results

| | A — LLM end-to-end | B — Honest Mirror (NAL + receipt) |
|---|---|---|
| recovers the core | usually — but phrasing varies every run | yes, exactly |
| inference receipt | none | full |
| reproducible | no (3 runs → 3 distinct answers) | yes (deterministic) |

Branch B (identical across runs):

```
tension term : (--> raskolnikov above-ordinary-morality)   f=0.34 c=0.77  REJECT
abduced      : (--> raskolnikov bound-by-conscience)        f=0.82 c=0.41  HYPOTHESIZE
supported by : [article-pravo-imeyu] [marmeladov-last-money] [conscience-illness-after] [confession-yavka]
```

The contested truth-value sits near 0.5 with *rising* confidence — the signature of a genuine STATED↔ENACTED contradiction (claims cancel; evidence accumulates). The abduced commitment is the Immunity-to-Change reading of the same data: the behaviour that undermines the stated value points to a hidden commitment.

## 4. Interpretation

- **Verifiable discernment.** B's answer is the same every time *and* comes with a trail a human (or another agent) can check premise by premise. A's cannot be audited or corrected.
- **Honesty is structural.** NAL abduction's confidence ceiling (~0.45) means a surfaced tension is permanently a **hypothesis**, never a verdict — by construction, not by prompt discipline. The system is built so it *cannot* over-claim about a person.
- **Self-opacity is expensive, on purpose.** A scheduled cross-context collision (axis B) forces compartmentalised claims to meet, so a contradiction is *found*, not waited for.

## 5. Limitations (stated plainly)

- Extraction is the weak link (LLM swaps subject/predicate, over-estimates confidence); we cap input confidence at 0.5 and hand-verify the benchmark atoms. Auto-extraction quality is future work.
- AtomSpace is ephemeral per call; durability is the vector store. Provenance is held in a side-map (the NAL term must match for revision to fire).
- One character, one tension per surface, by design (sprint scope). Generalisation across many people/atoms is the next axis.

## 6. Fit

Track 1, plugin-style — extends OmegaClaw without touching its core, and leans into the sprint theme *agents that hold the thread*: a durable, inspectable, uncertainty-aware model of a person.

> _[operator: optional — drop in a verbatim quote from Ben's BGI opening keynote on long-term memory / identity-feel being OmegaClaw's main payoff, with source, here.]_

## 7. Who it's for, continuation, safety

**Intended consumers.** OmegaClaw maintainers (a reusable pattern for NAL reasoning + side-map provenance from a skill); developers building agents (verifiable, reproducible judgments with a receipt); BGI/coherence researchers (a runnable value-coherence benchmark).

**What's complete / next.** Complete: pipeline on the engine, Mayor-N demo, Raskolnikov A/B with ground truth, registered skill, this note. Next: auto-extraction quality (atoms are hand-verified for the benchmark), richer inspection-view, generalisation across many atoms/people, multi-tension surfacing. Continuation is cheap — the benchmark is one file and the pipeline is modular.

**Safety.** Reasoning about a person's values is kept honest by construction: abduction is confidence-capped (a question, not a verdict), grounding is human-in-the-loop, no real personal data without consent (synthetic mayor + public-domain character), and this is a reflection aid — not a diagnostic or scoring tool.

---
*The Honest Mirror · BGI Sprint 1 · MIT.*
