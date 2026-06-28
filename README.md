# The Honest Mirror

### *Crime and Discernment — an OmegaClaw skill that judges a person and refuses to sentence them.*

**BGI Sprint 1 · Track 1 (extends OmegaClaw) · MIT**

> *"the architecture forces honesty defects to be observable"*
> — Ben Goertzel, [*Wild Times in the AGI Lab*](https://bengoertzel.substack.com/p/wild-times-in-the-agi-lab) (Substack, 2026) — the article that inspired this project's forced cross-context collision.

> 📄 **[Read the full research note →](docs/research-note.md)** — the complete study: method, the maturity-trajectory result, the A/B benchmark, the pattern math, and the ethics. *This README is the tour; the [research note](docs/research-note.md) is the whole thing.*

Porfiry Petrovich never arrests Raskolnikov. He sets the man's grand theory beside the man's actual deeds and waits for him to arrive at himself. The Honest Mirror does the same, in atoms: it surfaces a person's sharpest value-tension as a **hypothesis with a receipt**, and — by construction — never as a verdict. Call it **Porfiry-as-a-Service**.

> *Theme fit ("agents that hold the thread"): the agent keeps a durable, inspectable model of who you are and reasons over it under uncertainty — instead of re-hallucinating a personality every turn.*

> **New to the novel?** *Crime and Punishment* — [free at Project Gutenberg](https://www.gutenberg.org/ebooks/2554). Raskolnikov, a destitute ex-student, murders a pawnbroker to prove a theory: that *extraordinary* people hold **the right** (*право имею*, "I have the right") to step over ordinary morality for a higher end. The rest of the book is his own conscience refuting the theory. Porfiry is the magistrate who never arrests him — he just sets the theory beside the deeds and waits.

## The headline: we watched Raskolnikov grow up — on a graph

Most "personality" demos hand you one fluent paragraph. We hand you a **trajectory**. Slice *Crime and Punishment* into five snapshots, run the maturity lens (Action Logic) on each, and track two terms as the novel moves:

![Raskolnikov's maturity arc](docs/trajectory.png)

| slice | theory · `above-ordinary-morality` | conscience · `bound-by-conscience` |
|---|---|---|
| 1 · the article, the murder as proof | **f 0.69** | f 0.30 |
| 2 · the Marmeladovs, the fever after | f 0.57 | f 0.46 |
| 3 · the duels with Porfiry | f 0.54 | **f 0.56**  ← they cross |
| 4 · Sonya, the confession | f 0.49 | f 0.67 |
| 5 · the surrender, Siberia | f 0.44 | **f 0.73** |

The theory of *право имею* falls monotonically; conscience rises and overtakes it at slice 3 — Raskolnikov's maturation made legible as a **curve**, deterministic across runs, with a per-slice receipt behind every point. The curve isn't hand-drawn: every atom enters at `c = 0.45`, and the engine computes the shape from the balance of evidence. He spent six hundred pages arguing whether he was Napoleon or a louse; the engine declines to settle it for him, and shows the line along which he settles it himself.

## Why this beats a bare LLM

Ask a stateless model "what is this person's core contradiction?" and you get a sentence — fluent, plausible, different every run, with no trail. We call that **confidence laundering**. `bench/run_ab.py` runs the *same* atoms two ways against a ground-truth core from literary criticism:

| | A — LLM end-to-end | B — Honest Mirror (NAL + receipt) |
|---|---|---|
| recovers the core | usually — but phrased differently each run | **yes, exactly** |
| inference receipt | none | **full** |
| reproducible | no (3 runs → 3 answers) | **yes** |

```
— receipt (branch B, identical every run) —
tension : (--> raskolnikov above-ordinary-morality)  f=0.34 c=0.77  REJECT (CONTESTED)
abduced : (--> raskolnikov bound-by-conscience)       f=0.82 c=0.41  HYPOTHESIZE
why     : [article-pravo-imeyu] [marmeladov-last-money] [conscience-illness-after] [confession-yavka]
```

The theory and the conscience collide on one NAL term; revision drives frequency toward 0.5 while confidence climbs (the signature of a real contradiction); abduction names the hidden commitment — and stops, capped, as a question.

## Run it in ~10 minutes

Needs the OmegaClaw container (it carries the PeTTa engine). The skill is mounted at `/tmp/honest-mirror`.

```bash
# the headline — maturity arc across five slices → docs/trajectory.json + trajectory.png
docker exec -e PYTHONPATH=/PeTTa/repos/OmegaClaw-Core \
  omegaclaw python3 /tmp/honest-mirror/bench/trajectory.py

# the A/B — symbolic vs LLM on the same atoms
docker exec -e PYTHONPATH=/PeTTa/repos/OmegaClaw-Core \
  omegaclaw python3 /tmp/honest-mirror/bench/run_ab.py

# the reproducible synthetic-mayor demo — tension + receipt
docker exec -e PYTHONPATH=/PeTTa/repos/OmegaClaw-Core \
  omegaclaw python3 /tmp/honest-mirror/skill/honest_mirror.py
```

As registered agent commands:

| command | runs |
|---|---|
| `honest-mirror-trajectory` | the maturity arc (the headline) |
| `honest-mirror-raskolnikov` | the single-contradiction benchmark |
| `honest-mirror-demo` | synthetic Mayor N |
| `honest-mirror "<text>"` | any reflection — e.g. about yourself |

**The live modes, in plain terms.** Beyond the two benchmarks, the skill runs as an everyday agent capability inside OmegaClaw:

- **`honest-mirror-demo` — Mayor N.** A *synthetic* city leader (no real person, no consent problem). His inaugural speech says *"we're a team, we listen to citizens"*; his meeting notes say *"decided the budget alone under pressure, took the failing project onto myself, keep re-checking my deputies."* The skill collides the two and surfaces the tension — *under pressure he returns to sole control, though he values the team* — then abduces the hidden commitment beneath it (*"to delegate is to risk what only I will answer for"*), as a question, with a receipt. This is the one a reviewer runs first.
- **`honest-mirror-raskolnikov` — the benchmark character** (the arc and A/B above).
- **`honest-mirror "<text>"` — bring your own.** Drop in any reflection — a diary entry, a decision write-up, your own — and get a single surfaced tension with its trail. The mirror is general; Mayor N and Raskolnikov are just two faces standing in front of it.

## Under the hood (the honest version)

One LLM step — extraction — capped at confidence 0.5, because that is the noisy link. Everything after is symbolic and reproducible on the real NAL engine (`|-`, PeTTa / MeTTa-on-SWI-Prolog), one fresh AtomSpace per call. **Revision** accumulates confidence on a durable term; a **forced cross-context collision** makes a person's compartmentalised claims meet (self-opacity, made expensive); **abduction is capped at ~0.45**, so a finding is permanently a hypothesis. The AtomSpace is ephemeral — it forgets itself every call — so we hold the thread with three compensations: revision (confidence), a side-map (provenance), and a vector store (memory). Full write-up: **`docs/research-note.md`**.

## One engine, six patterns, many lenses

**What's in the core.** Exactly one step uses the LLM — extraction: text → atoms `((--> subject predicate) (stv f c))`, capped at `c = 0.5`. After that it is pure NAL on the `|-` engine, the same pipeline every time:

```
EXTRACT → SEED → REVISE → COLLIDE → ABDUCE → GATE → SURFACE → GROUND
```

A "pattern" is simply a *question* asked over those atoms. The engine never changes between patterns — only the **target** changes (and the lens that dresses the output). What we always *compute* is a truth-value `(f, c)` with provenance, gated into `ACT / HYPOTHESIZE / IGNORE`. Contradiction is the first pattern, not the only one:

| Pattern | What we compute | Status |
|---|---|---|
| **Contradiction** (STATED ↔ ENACTED) | both land on one term; revision drives `f → ~0.5` while `c` keeps rising → a CONTESTED truth-value (claims cancel, evidence stacks) | ✅ wired |
| **Trajectory / growth** | track one term across time-slices → a *series* of `(f, c)` → the curve and where it crosses | ✅ wired — *the headline* |
| **Undisclosed potential** (ENACTED > STATED) | reverse abduction — a capacity enacted but never claimed → a strength hypothesis with provenance, same `~0.45` ceiling | designed |
| **Blind spot / distortion** | a stated inference whose support never accumulates → `c` stays low however often it repeats | designed |
| **Coherence** | claims that *agree* across compartments → high `f`, high `c`, no collision → name the wholeness, not only the cracks | designed |
| **Readiness / maturation** | a term climbing toward the next-stage threshold → an "approaching ACT" signal | designed |

This sprint wires the two that prove the thesis — **contradiction** (the single-point benchmark) and **trajectory** (the arc). The other four are designed and described, because the claim under test is the *engine*, not the catalogue. **Full mechanics, the pattern math, and the lens set → [`docs/research-note.md`](docs/research-note.md).**

A **lens** (Action Logic, Immunity to Change, Four Dimensions, Four Voices, Moral Foundations) is a swappable module: it sets *which atoms we extract*, *what counts as a tension*, and *the output form* — over an engine that stays invariant. The maturity arc above reads through Action Logic; the single-point benchmark reads the same atoms through Immunity to Change. Same engine, different lens.

## Safety

It reasons about a person, so it under-claims by *arithmetic*, not by manners: a finding is a hypothesis, never a verdict (the ceiling is structural); the human sees the atoms and can refute them (grounding); no real personal data without consent (a synthetic mayor and a public-domain character); a reflection aid, not a diagnostic or scoring tool.

## Track 1 fit — *Improvements to OmegaClaw*

A plugin-style skill that does not touch the core (`honest-mirror-*` registered in `src/skills.metta`); a benchmark plus a trajectory result (`bench/`); a flaw-detection-and-grounding workflow; deterministic, reproducible runs as acceptance criteria.

## Layout

```
skill/   honest_mirror.py · nal_ops.metta · collision.metta · skills.metta
data/    mayor_atoms.metta · commitments.metta · raskolnikov_atoms.metta · raskolnikov_slices/ · *_source.md · *_ground_truth.md
bench/   run_ab.py · trajectory.py
viz/     plot_trajectory.py
docs/    research-note.md · trajectory.json · trajectory.png
```

## Licence

[MIT](LICENSE) © 2026 Alexander Maneev
