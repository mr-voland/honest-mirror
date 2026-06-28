#!/usr/bin/env python3
"""trajectory.py — Raskolnikov maturity TRAJECTORY across 5 slices (kill-feature).

Thesis: one discernment engine over ephemeral atoms builds a *trajectory* of
development (not a one-off judgement) — what a bare LLM gives as a "floating"
retelling without a receipt.

We track two terms as evidence ACCUMULATES slice by slice (cumulative revision):
  theory     = (--> raskolnikov above-ordinary-morality)   — expect f DOWN
  conscience = (--> raskolnikov bound-by-conscience)        — abduced, f & c UP
The crossover slice (conscience f overtakes theory f) is the maturity turn.

Per-atom c is uniform (0.45) in the slice files: the trend and the rising
confidence EMERGE from accumulation (count + STATED/ENACTED balance) computed by
the engine's NAL revision — it is NOT a hand-drawn curve.

Run inside the OmegaClaw container (engine available):
  docker exec -e PYTHONPATH=/PeTTa/repos/OmegaClaw-Core omegaclaw \
      python3 /tmp/honest-mirror/bench/trajectory.py
"""
import os
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "skill"))
import honest_mirror as hm  # noqa: E402

SLICES_DIR = os.path.join(ROOT, "data", "raskolnikov_slices")
COMMITS = os.path.join(ROOT, "data", "commitments.metta")

SLICE_FILES = ["slice1.metta", "slice2.metta", "slice3.metta", "slice4.metta", "slice5.metta"]
SLICE_LABELS = [
    "Ч.1 — статья «право имею» + убийство",
    "Ч.1–2 — последние деньги Мармеладовым; болезнь совести",
    "Ч.3–4 — дуэли с Порфирием",
    "Ч.5 — Соня, признание ей; контраст с Лужиным",
    "Эпилог — явка, Сибирь, поворот к Соне",
]

THEORY_TERM = "(--> raskolnikov above-ordinary-morality)"
THEORY_PRED = "above-ordinary-morality"
CONSCIENCE_COMMITMENT = "bound-by-conscience"
CONSCIENCE_TERM = "(--> raskolnikov bound-by-conscience)"


def _writable_out():
    """First writable dir for the artifacts (docs/ locally; memory volume in-container)."""
    cands = [
        os.environ.get("TRAJECTORY_OUT"),
        os.path.join(ROOT, "docs"),
        "/PeTTa/repos/OmegaClaw-Core/memory/trajectory",
        "/tmp/honest-mirror-trajectory",
    ]
    for base in cands:
        if not base:
            continue
        try:
            os.makedirs(base, exist_ok=True)
            probe = os.path.join(base, ".wtest")
            with open(probe, "w") as fh:
                fh.write("")
            os.unlink(probe)
            return base
        except Exception:
            continue
    return ROOT


def _fold_term(engine, atoms, term):
    """Accumulated belief in `term` = revision folded over ALL its atoms.
    NAL revision is order-independent in weight space, so folding STATED (high f)
    with ENACTED (low f) yields the confidence-weighted belief; as low-f ENACTED
    evidence accumulates, f drifts down and c rises."""
    grp = [o for o in atoms if o.term == term]
    if not grp:
        return None, []
    tv = grp[0].tv
    for o in grp[1:]:
        tv = engine.revise2(term, tv, o.tv)
    prov = [o.src.strip("[]") for o in grp if o.src]
    return tv, prov


def _conscience(engine, atoms, commits):
    """Abduced (--> raskolnikov bound-by-conscience) from accumulated acts-from-conscience."""
    abds = hm.abduce_commitment(engine, atoms, commits)
    hit = next((a for a in abds if a["commitment"] == CONSCIENCE_COMMITMENT), None)
    if not hit:
        return None, []
    prov = [o.src.strip("[]") for o in atoms
            if o.pred == hit["behaviour"] and o.role == "ENACTED" and o.src]
    return hit["hyp"], prov


def build_trajectory(write=True):
    """Run the engine over cumulative slices; return the trajectory dict."""
    engine = hm.MirrorEngine()
    commits = hm.load_commitments(COMMITS)
    cumulative = []
    slices = []
    crossover = None
    for i, fname in enumerate(SLICE_FILES, 1):
        cumulative += hm.load_atoms_metta(os.path.join(SLICES_DIR, fname))
        th_tv, th_prov = _fold_term(engine, cumulative, THEORY_TERM)
        co_tv, co_prov = _conscience(engine, cumulative, commits)
        entry = {
            "slice": i,
            "label": SLICE_LABELS[i - 1],
            "theory": {
                "term": THEORY_TERM,
                "f": round(th_tv[0], 4) if th_tv else None,
                "c": round(th_tv[1], 4) if th_tv else None,
                "gate": hm.gate(th_tv) if th_tv else None,
                "provenance": th_prov,
            },
            "conscience": {
                "term": CONSCIENCE_TERM,
                "f": round(co_tv[0], 4) if co_tv else None,
                "c": round(co_tv[1], 4) if co_tv else None,
                "gate": hm.gate(co_tv) if co_tv else None,
                "provenance": co_prov,
            },
        }
        if (crossover is None and th_tv and co_tv and co_tv[0] >= th_tv[0]):
            crossover = i
        slices.append(entry)
    data = {
        "character": "raskolnikov",
        "lens": "Action Logic (maturity; Cook-Greuter/Torbert)",
        "terms": {"theory": THEORY_TERM, "conscience": CONSCIENCE_TERM},
        "crossover_slice": crossover,
        "slices": slices,
    }
    if write:
        out = _writable_out()
        path = os.path.join(out, "trajectory.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        data["_json_path"] = path
    return data


def _print_table(data):
    print("=" * 72)
    print("THE HONEST MIRROR — Raskolnikov maturity trajectory")
    print("=" * 72)
    print(f"{'slice':<6}{'theory f (c) gate':<30}{'conscience f (c) gate':<30}")
    print("-" * 72)
    for s in data["slices"]:
        t, c = s["theory"], s["conscience"]
        ts = f"{t['f']:.2f} ({t['c']:.2f}) {t['gate']}"
        cs = f"{c['f']:.2f} ({c['c']:.2f}) {c['gate']}"
        mark = "  <- перелом" if data["crossover_slice"] == s["slice"] else ""
        print(f"{s['slice']:<6}{ts:<30}{cs:<30}{mark}")
    print("-" * 72)
    print(f"crossover (совесть обгоняет теорию): срез {data['crossover_slice']}")
    if data.get("_json_path"):
        print(f"json: {data['_json_path']}")


def main():
    data = build_trajectory(write=True)
    _print_table(data)
    # best-effort plot (pure function of the json; works outside the container too)
    try:
        sys.path.insert(0, os.path.join(ROOT, "viz"))
        import plot_trajectory  # noqa: E402
        png = plot_trajectory.plot(data.get("_json_path"), None)
        print(f"png:  {png}")
    except Exception as e:
        print(f"[plot skipped: {e}]")


if __name__ == "__main__":
    main()
