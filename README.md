# The Honest Mirror

**BGI Sprint 1 · Track 1 (extends OmegaClaw) · 26–28 June 2026**

An OmegaClaw skill that atomises a person's reflection into NAL, surfaces their **single sharpest value-contradiction** as a *hypothesis with a full inference receipt*, and lets them inspect and correct what the agent believes about them — something a stateless LLM cannot do.

> Theme fit ("agents that hold the thread"): the agent keeps a durable, inspectable model of *who you are* and reasons over it under uncertainty, instead of re-deriving a personality from scratch each turn.

## The idea in one screen

A reflection contains what a person **states** about their values and what their action-narratives **enact**. When these diverge on the *same* value, that is a contradiction worth surfacing — but honestly, as a question, not a verdict.

```
EXTRACT  reflection → NAL atoms  ((--> subj pred) (stv f c)),  c ≤ 0.5 (LLM tier)
REVISE   same-term atoms → NAL revision accumulates confidence
COLLIDE  STATED vs ENACTED on one term → CONTESTED (f→0.5, c↑)   [forced cross-context collision]
ABDUCE   the contested behaviour → hidden competing commitment (c ceiling ≈0.45)
GATE     ACT (f≥0.6 ∧ c≥0.5) / HYPOTHESIZE (f≥0.3 ∧ c≥0.2) / IGNORE
SURFACE  one tension + receipt (premises · rule · stv · gate)
GROUND   human confirms/refutes → new premise → revision next cycle
```

Reasoning runs on the **real NAL engine** (`|-` in OmegaClaw's PeTTa / MeTTa-on-SWI-Prolog), one fresh AtomSpace per call. Extraction is the only LLM step; the contradiction logic is symbolic and reproducible.

## Why this beats a stateless LLM (the benchmark)

`bench/run_ab.py` runs the **same** atomised input two ways on Raskolnikov (*Crime and Punishment*, public domain), against a ground-truth core from literary criticism:

| | A — LLM end-to-end | B — Honest Mirror (NAL + receipt) |
|---|---|---|
| recovers the core | usually, but **phrasing varies every run** | **yes, exactly** |
| inference receipt | none | **full** (premises → rule → truth-value → gate) |
| reproducible | **no** (3 runs → 3 different answers) | **yes** (deterministic) |

Branch B output (deterministic):

```
— receipt —
tension term : (--> raskolnikov above-ordinary-morality)
contested    : f=0.34 c=0.77  (REJECT)
supported by : [article-pravo-imeyu], [marmeladov-last-money], [conscience-illness-after], [confession-yavka]
abduced      : (--> raskolnikov bound-by-conscience)  f=0.82 c=0.41
gate         : HYPOTHESIZE  (abduction is capped ~0.45 -> hypothesis)
```

i.e. the theory of "право имею" (the right to transgress morality) collides with his own conscience-bound nature — the canonical contradiction — surfaced with a checkable trail, not just a sentence.

## Run it in ~10 minutes

Requires the OmegaClaw container (it carries the PeTTa engine + providers). The skill is mounted at `/tmp/honest-mirror`.

```bash
# 1) reproducible Mayor-N demo (synthetic) — tension + receipt
docker exec -e PYTHONPATH=/PeTTa/repos/OmegaClaw-Core \
  omegaclaw python3 /tmp/honest-mirror/skill/honest_mirror.py

# 2) Raskolnikov A/B benchmark — symbolic vs LLM baseline
docker exec -e PYTHONPATH=/PeTTa/repos/OmegaClaw-Core \
  omegaclaw python3 /tmp/honest-mirror/bench/run_ab.py

# 3) as a registered agent command (from the bot / a MeTTa REPL)
#    honest-mirror-demo        → runs the Mayor-N demo through the engine
#    honest-mirror "<text>"    → atomise + surface a tension for arbitrary text
```

Expected Mayor-N output: `relies-on-team` CONTESTED (REJECT, f≈0.36 c≈0.77) → abduced `protect-sole-accountability` (f≈0.82 c≈0.41, HYPOTHESIZE).

## Populations

| Tier | Purpose |
|---|---|
| Synthetic Mayor N | Demo — reviewer runs it immediately (`data/mayor_atoms.metta`) |
| Raskolnikov | Benchmark with ground truth + LLM baseline (`data/raskolnikov_*`) |
| Self (optional) | Live reflection via the Telegram agent |

## Who it's for

- **OmegaClaw maintainers / contributors** — a clean, plugin-style example of doing real NAL reasoning (`|-`) from a skill, with a side-map provenance pattern others can reuse.
- **Developers building agent systems** — a reproducible pattern for *verifiable* judgments (deterministic + receipt) instead of unauditable LLM verdicts.
- **BGI / coherence researchers** — a runnable testbed and benchmark for value-coherence reasoning over human reflection.

## Track 1 fit — *Improvements to OmegaClaw*

This is a concrete, buildable improvement to OmegaClaw that respects the core boundary. It lands squarely on the track's example contributions:

| Track 1 example | Here |
|---|---|
| Plugin-style extension that doesn't touch the core | `honest-mirror` / `honest-mirror-demo` registered in `src/skills.metta`; core untouched |
| Benchmarking and evaluation tools | `bench/run_ab.py` — symbolic vs LLM A/B with ground truth |
| Flaw detection and correction workflows | surfaces a value-contradiction, then **grounds** it via human confirm/refute → revision |
| Tests / validation frameworks | acceptance criteria + a deterministic, reproducible run |

**Evidence it works (acceptance criteria):** the Mayor-N demo and the Raskolnikov benchmark above are deterministic and reproduce the documented numbers on every run (`f=0.34 c=0.77 REJECT` → `bound-by-conscience f=0.82 c=0.41 HYPOTHESIZE`); branch B recovers the ground-truth core, branch A does not reproduce.

## Honest constraints

- AtomSpace is ephemeral per `|-` — durability is ChromaDB (`remember`/`query`); provenance lives in a side-map because the NAL term must match for revision to fire.
- Abduction confidence is structurally capped (~0.45) — a surfaced tension is permanently a **question**, never a verdict. This is a feature (honesty over certainty), not a bug.
- LLM extraction is noisy (subject/predicate swaps, over-confidence) → input confidence capped at 0.5; the benchmark uses hand-verified atoms.
- PLN abduction returns empty in this build — all inference is NAL.

## Safety & ethics

This skill reasons about a person's values, so it is built to under-claim by design:
- A surfaced tension is always a **hypothesis, never a verdict** — abduction confidence is structurally capped (~0.45), so the system cannot assert a conclusion about someone.
- **Human-in-the-loop grounding:** the person sees the atoms and confirms or refutes; their input is the source of truth.
- **No real personal data** is used without explicit consent — the demo is a synthetic mayor; the benchmark is a public-domain literary character.
- It is a reflection aid, **not** a diagnostic, clinical, or scoring tool, and is not for covert profiling.

## Status & continuation

**Complete (this sprint):** NAL pipeline on the real engine (`|-`); Mayor-N demo; Raskolnikov A/B benchmark with ground truth; skill registered and callable; README + research note.

**Not yet / next:** auto-extraction quality (currently hand-verified atoms for the benchmark); a richer inspection-view (text dump of held atoms + feedback loop); generalisation across many atoms/people; multi-tension surfacing.

**Who should review it next:** OmegaClaw maintainers (skill/reasoning pattern) and BGI coherence researchers (benchmark methodology). Continuation is straightforward — the pipeline is modular and the benchmark is one file.

## Layout

```
skill/   honest_mirror.py · nal_ops.metta · collision.metta · skills.metta
data/    mayor_atoms.metta · commitments.metta · raskolnikov_atoms.metta · *_source.md · *_ground_truth.md
bench/   run_ab.py
docs/    research-note.md · video-script.md
```

## Licence

[MIT](LICENSE) © 2026 Alexander Maneev
