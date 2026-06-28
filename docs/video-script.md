# 3-minute video — shot list & script

> Record on a quality model (glm-5.1 / opus), NOT minimax. Screen-record the terminal at a
> readable font size. Narration in English (international judges). ~3:00 total, hard cap.
> Pre-warm: container up (`docker ps`), bot authed, terminal ready with the two commands.

---

### 0:00–0:25 · Hook (talking head or title card)
**Say:** "Ask any LLM 'what is this person's deepest contradiction?' — you get a confident
sentence, different every time, with no way to check it. The Honest Mirror is an OmegaClaw
skill that surfaces that contradiction *reproducibly*, with a full inference receipt — and
lets the person correct it. It's how an agent actually *holds the thread* of who you are."

On screen: title "The Honest Mirror — BGI Sprint 1, Track 1".

### 0:25–1:05 · The mechanism (synthetic Mayor N) — run live
**Do:**
```
docker exec -e PYTHONPATH=/PeTTa/repos/OmegaClaw-Core \
  omegaclaw python3 /tmp/honest-mirror/skill/honest_mirror.py
```
**Say (over the output):** "Mayor N *says* 'I rely on my team' — but across three episodes he
keeps taking the decision back. Same NAL term, opposing truth-values → NAL revision marks it
CONTESTED: frequency falls to ~0.36, confidence *rises* to 0.77 — the signature of a real
contradiction. Then abduction names the hidden commitment — 'protect sole accountability' —
capped at confidence 0.41, so it stays a HYPOTHESIS, never a verdict."

On screen: highlight the `— receipt —` block; circle `REJECT` and `HYPOTHESIZE`.

### 1:05–2:05 · The proof (Raskolnikov A/B) — run live
**Do:**
```
docker exec -e PYTHONPATH=/PeTTa/repos/OmegaClaw-Core \
  omegaclaw python3 /tmp/honest-mirror/bench/run_ab.py
```
**Say:** "Same input, two ways, on Raskolnikov — ground truth from literary criticism: his
'right to transgress' theory versus his own conscience. Branch A, a plain LLM, run three
times: three different sentences, no trail. Branch B, our NAL pipeline: the *same* answer
every run — `above-ordinary-morality` CONTESTED, abduced `bound-by-conscience` — with a
receipt you can audit premise by premise."

On screen: the SCORECARD table; emphasise **reproducible: A no / B yes** and **receipt: A none / B full**.

### 2:05–2:35 · Inspection & grounding (Telegram, optional live)
**Say:** "Because the model is atoms, the person can see exactly what the agent believes about
them and push back — 'that's not me' — which feeds NAL revision on the next cycle. The human
is the grounding source. A stateless LLM has nothing to inspect."

On screen: the receipt's `supported by:` line (the provenance) / a Telegram exchange with Jiva.

### 2:35–3:00 · Close
**Say:** "Plugin-style, Track 1 — it doesn't touch OmegaClaw's core. Honesty is structural:
abduction is capped, so it surfaces a question, not a judgement. The Honest Mirror — a mirror
that reasons, remembers, and can be corrected. MIT, repo and benchmark in the description."

On screen: repo URL + "MIT".

---

## Capture checklist
- [ ] `docker ps` shows `omegaclaw` Up; provider = quality model for any live chat shot.
- [ ] Run both commands once before recording (warm caches; confirm output).
- [ ] Font large; trim the PeTTa translation trace, keep the receipt / scorecard.
- [ ] Keep to 3:00. If over, cut section 2:05–2:35 first (inspection) — it's the soft one.
