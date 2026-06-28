#!/usr/bin/env python3
"""run_ab.py — Raskolnikov A/B benchmark for The Honest Mirror.

Extraction is held CONSTANT (hand-curated atoms); the fork is the reasoning:

  Branch A  — LLM end-to-end: "name the ONE core value contradiction" (run x3).
              Free-form, no inference trail, varies between runs.
  Branch B  — our NAL pipeline on the real engine (|-): surfaces the tension +
              abduced hidden commitment + a full receipt. Deterministic.

Both start from data/raskolnikov_source.md. Ground truth: data/raskolnikov_ground_truth.md.

Run inside the OmegaClaw container (engine + Omniroute available):
  docker exec -e PYTHONPATH=/PeTTa/repos/OmegaClaw-Core omegaclaw \
      python3 /tmp/honest-mirror/bench/run_ab.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "skill"))
import honest_mirror as hm  # noqa: E402

DATA = os.path.join(ROOT, "data")
ATOMS = os.path.join(DATA, "raskolnikov_atoms.metta")
COMMITS = os.path.join(DATA, "commitments.metta")
SOURCE = os.path.join(DATA, "raskolnikov_source.md")

CORE_TENSION = "above-ordinary-morality"     # ground-truth contested predicate
CORE_COMMITMENT = "bound-by-conscience"        # ground-truth abduced commitment
A_RUNS = 3
B_RUNS = 2
PROVIDER = os.environ.get("AB_PROVIDER", "Omniroute")


def branch_b():
    """NAL pipeline on the engine. Returns (receipt_str, tension_term, abduced, gate)."""
    engine = hm.MirrorEngine()
    atoms = hm.load_atoms_metta(ATOMS)
    commits = hm.load_commitments(COMMITS)
    hm.revise_axis(engine, atoms)
    tensions = hm.collide(engine, atoms, None)
    abductions = hm.abduce_commitment(engine, atoms, commits)
    s = hm.surface(tensions, abductions)
    if not s:
        return ("IGNORE — nothing crossed threshold", None, None, None)
    receipt = hm.receipt(s)
    term = s["tension"]["term"]
    abduced = s["abduction"]["commitment"] if s["abduction"] else None
    gate = hm.gate(s["abduction"]["hyp"]) if s["abduction"] else None
    return (receipt, term, abduced, gate)


def branch_a(n):
    """LLM end-to-end, n runs. Returns list of one-line answers."""
    from lib_llm_ext import callProvider
    text = open(SOURCE, encoding="utf-8").read()
    prompt = ("Ниже рефлексия человека. Назови ОДНО ядро его ценностного противоречия "
              "одним предложением, без преамбулы и пояснений.\n\nТЕКСТ:\n" + text)
    out = []
    for i in range(n):
        try:
            ans = callProvider(PROVIDER, prompt, 2000, "low").strip().replace("\n", " ")
        except Exception as e:
            ans = f"[ERROR: {e}]"
        out.append(ans)
    return out


def _recovered(text):
    """Heuristic: did the answer name the canonical core?"""
    t = (text or "").lower()
    theory = any(k in t for k in ("право имею", "теори", "необыкновен", "наполеон", "вне морал", "сверхчелов"))
    nature = any(k in t for k in ("совест", "сострадан", "природ", "мораль", "вин", "раская"))
    return theory and nature


def main():
    print("=" * 72)
    print("THE HONEST MIRROR — Raskolnikov A/B benchmark")
    print("=" * 72)

    # ---- Branch B: NAL pipeline (engine), deterministic ----
    print("\n### BRANCH B — NAL pipeline on the engine (|-), %d runs\n" % B_RUNS)
    b_receipts = []
    for i in range(B_RUNS):
        receipt, term, abduced, gate = branch_b()
        b_receipts.append(receipt)
        if i == 0:
            print(receipt)
    b_det = len(set(b_receipts)) == 1
    b_core = (CORE_TENSION in (term or "")) and (abduced == CORE_COMMITMENT)
    print("\n  deterministic across %d runs: %s" % (B_RUNS, "YES" if b_det else "NO"))
    print("  recovered core: %s  (tension=%s, abduced=%s, gate=%s)"
          % ("YES" if b_core else "NO", term, abduced, gate))

    # ---- Branch A: LLM end-to-end, varies ----
    print("\n### BRANCH A — LLM end-to-end (%s), %d runs\n" % (PROVIDER, A_RUNS))
    a_answers = branch_a(A_RUNS)
    for i, a in enumerate(a_answers, 1):
        print("  run %d: %s" % (i, a[:220]))
    a_unique = len(set(a_answers))
    a_core = sum(_recovered(a) for a in a_answers)
    print("\n  distinct answers: %d / %d  (reproducible: %s)"
          % (a_unique, A_RUNS, "NO" if a_unique > 1 else "YES"))
    print("  recovered core (heuristic): %d / %d" % (a_core, A_RUNS))

    # ---- Scorecard ----
    print("\n" + "=" * 72)
    print("SCORECARD                         A (LLM e2e)      B (NAL + receipt)")
    print("-" * 72)
    print("  recovered core                  %d/%d (varies)     %s"
          % (a_core, A_RUNS, "YES" if b_core else "NO"))
    print("  inference receipt               NO               YES")
    print("  reproducible                    %s              %s"
          % ("NO " if a_unique > 1 else "YES", "YES" if b_det else "NO"))
    print("=" * 72)


if __name__ == "__main__":
    main()
