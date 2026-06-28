"""
honest_mirror.py — The Honest Mirror skill (orchestrator)
=========================================================
OmegaClaw plugin-style skill. Surfaces ONE value tension from reflection text
as a HYPOTHESIS with a full inference receipt, and (axis B) forces hidden
contradictions between compartments to collide.

Design (verified against C:\\_Dev\\OmegaClaw):
  - Atom form:  ((--> subj pred) (stv f c)).  |- is BINARY.
  - Contradiction lives on ONE term (STATED vs ENACTED truths, same predicate).
  - Provenance (STATED/ENACTED + source) is a Python side-map, NOT inside the atom
    (the NAL term must match exactly for revision to fire).
  - REASONING runs on the real NAL engine via |- on a FRESH MeTTa instance per
    call (this is our ephemeral-AtomSpace property, by construction).
  - Extraction = LLM via lib_llm_ext.callProvider. Persistence = remember/query.

Pipeline:  EXTRACT -> SEED -> REVISE -> COLLIDE(axisB) -> ABDUCE -> GATE -> SURFACE -> GROUND

Run paths:
  run(text)  — live: extract atoms from text, then pipeline.
  demo()     — reproducible: load data/mayor_atoms.metta + data/commitments.metta.

VERIFY-in-WSL markers flag the spots that need a live MeTTa REPL to confirm
(hyperon import path, lib_nal load path, |- result string format).
"""

import os
import re
import subprocess
import tempfile

# --- paths (verified against the live OmegaClaw container, 2026-06-28) --------
# The engine is PeTTa (MeTTa-on-SWI-Prolog), NOT hyperon. Reasoning runs by
# invoking `swipl -s <PeTTa>/src/main.pl -- <file.metta>` and parsing stdout.
# The OmegaClaw-Core runtime lives under /PeTTa/repos/OmegaClaw-Core (lib_nal,
# lib_llm_ext, memory, chroma_db); /PeTTa is the PeTTa core that hosts src/main.pl.
ROOT = os.environ.get("HONEST_MIRROR_ROOT", "/tmp/honest-mirror")
OMEGACLAW_ROOT = os.environ.get("OMEGACLAW_ROOT", "/PeTTa")
PETTA_ROOT = os.environ.get("PETTA_ROOT", "/PeTTa")


def _find(name, roots):
    """Resolve a runtime file across known layouts (handles OMEGACLAW_ROOT being
    either /PeTTa or /PeTTa/repos/OmegaClaw-Core — the task spec said the former,
    but lib_nal.metta actually lives under the latter)."""
    for base in roots:
        for rel in (name, os.path.join("repos", "OmegaClaw-Core", name)):
            p = os.path.join(base, rel)
            if os.path.exists(p):
                return p
    return os.path.join(roots[0], name)  # best-effort default


LIB_NAL = _find("lib_nal.metta", [OMEGACLAW_ROOT, PETTA_ROOT])
MAIN_PL = _find(os.path.join("src", "main.pl"), [PETTA_ROOT, OMEGACLAW_ROOT])
DATA = os.path.join(ROOT, "data")

_ANSI = re.compile(r"\x1b\[[0-9;]*m")

GATE_ACT = lambda f, c: f >= 0.6 and c >= 0.5
GATE_HYP = lambda f, c: f >= 0.3 and c >= 0.2

# near-half band for a CollisionToken = REJECT (behaviour can outweigh speech,
# so a real contradiction often lands ~0.35, not exactly 0.5).
NEAR_HALF = (0.30, 0.70)


# ===========================================================================
# NAL engine wrapper — runs |- on a fresh MeTTa instance (ephemeral AtomSpace)
# ===========================================================================
class MirrorEngine:
    """Drives the real PeTTa NAL engine by shelling out to swipl.

    Each |- runs on a FRESH process (our ephemeral-AtomSpace property, by
    construction): we write lib_nal.metta + one `!(|- ...)` line to a temp file
    and run `swipl -s <main.pl> -- <file>`. Output = a collapse SET of atoms;
    the member we want (matching the input term) is the FIRST one.
    """

    def __init__(self):
        with open(LIB_NAL, "r", encoding="utf-8") as fh:
            self._lib_nal = fh.read()

    def _run(self, sexpr: str) -> str:
        """Run one !(...) program through swipl, return the cleaned result line."""
        prog = self._lib_nal + "\n!(" + sexpr + ")\n"
        try:
            with tempfile.NamedTemporaryFile("w", suffix=".metta", delete=False,
                                             encoding="utf-8") as tf:
                tf.write(prog)
                path = tf.name
            proc = subprocess.run(
                ["swipl", "--stack_limit=8g", "-q", "-s", MAIN_PL, "--", path],
                capture_output=True, text=True, timeout=60)
            out = _ANSI.sub("", proc.stdout)
            # The evaluated !(...) results are printed last; pick the final line
            # that looks like a MeTTa result tuple (starts with "(").
            results = [ln.strip() for ln in out.splitlines()
                       if ln.strip().startswith("(")]
            return results[-1] if results else ""
        except Exception as e:
            print(f"[honest_mirror] |- run failed: {e}\n  sexpr: {sexpr}")
            return ""
        finally:
            try:
                os.unlink(path)
            except Exception:
                pass

    @staticmethod
    def _parse_stv(text: str, term: str):
        """Pull (stv f c) for `term` out of the |- collapse set.

        Verified format (2026-06-28): the engine returns one tuple of several
        atoms, e.g.
          (((--> mayorN relies-on-team) (stv 0.525 0.6206...)) ((--> ...) ...))
        The revision/abduction member that matches `term` is FIRST, so locating
        `term` and reading the nearest following (stv f c) is correct. Floats are
        full-precision; the regex tolerates that.
        """
        idx = text.find(term)
        chunk = text[idx:] if idx >= 0 else text
        m = re.search(r"\(stv\s+([0-9.eE+-]+)\s+([0-9.eE+-]+)\)", chunk)
        return (float(m.group(1)), float(m.group(2))) if m else None

    def revise2(self, term: str, tv1, tv2):
        """Revision of two SAME-TERM atoms via the engine."""
        a = f"({term} (stv {tv1[0]} {tv1[1]}))"
        b = f"({term} (stv {tv2[0]} {tv2[1]}))"
        out = self._run(f"|- {a} {b}")
        return self._parse_stv(out, term) or _py_revision(tv1, tv2)  # fallback = same math

    def abduce(self, commitment: str, behaviour: str, rule_tv, obs_tv, subj: str = "mayorN"):
        """((--> commitment behaviour) rule) + ((--> subj behaviour) obs) -> hidden."""
        rule = f"((--> {commitment} {behaviour}) (stv {rule_tv[0]} {rule_tv[1]}))"
        obs = f"((--> {subj} {behaviour}) (stv {obs_tv[0]} {obs_tv[1]}))"
        out = self._run(f"|- {rule} {obs}")
        term = f"(--> {subj} {commitment})"
        return self._parse_stv(out, term) or _py_abduction(rule_tv, obs_tv)


# --- pure-Python mirrors of the NAL truth functions (fallback / unit tests) ---
def _c2w(c):  return c / (1 - c) if c < 1 else 1e9
def _w2c(w):  return w / (w + 1)

def _py_revision(t1, t2):
    w1, w2 = _c2w(t1[1]), _c2w(t2[1])
    w = w1 + w2
    f = (w1 * t1[0] + w2 * t2[0]) / w
    c = min(0.99, max(_w2c(w), t1[1], t2[1]))
    return (round(min(1.0, f), 3), round(c, 3))

def _py_abduction(rule_tv, obs_tv):
    # Truth_Abduction((f1 c1),(f2 c2)) = (f2, w2c(f1*c1*c2))
    f = obs_tv[0]
    c = _w2c(rule_tv[0] * rule_tv[1] * obs_tv[1])
    return (round(f, 3), round(c, 3))


# ===========================================================================
# Atom layer (Python side-map holds provenance + role; NAL sees only term+truth)
# ===========================================================================
class Obs:
    __slots__ = ("subj", "pred", "f", "c", "role", "src")
    def __init__(self, subj, pred, f, c, role, src):
        self.subj, self.pred, self.f, self.c = subj, pred, f, c
        self.role, self.src = role, src   # role: STATED|ENACTED ; src: provenance tag
    @property
    def term(self): return f"(--> {self.subj} {self.pred})"
    @property
    def tv(self):   return (self.f, self.c)


# ===========================================================================
# EXTRACT — LLM text -> atoms (live path). Demo path loads pre-baked atoms.
# ===========================================================================
EXTRACT_PROMPT = """You convert a person's reflective text into NAL atoms about themselves.
Emit lines of the form:  ROLE | predicate | f | c | source
  ROLE = STATED (what they claim) or ENACTED (what their action-narratives show)
  predicate = a SHORT controlled token: relies-on-team, takes-control, leads-openly,
    withholds-vulnerability, wont-delegate, resists-dissent, defers-hard-decisions, ...
  f = 0..1 strength ;  c = confidence, MAX 0.5 (you over-estimate confidence)
Put a STATED claim and the contradicting ENACTED evidence on the SAME predicate.
Return only the lines, no prose."""

def extract(text: str, provider: str = "ASICloud"):
    """Live extraction. VERIFY: import path of callProvider inside container."""
    from lib_llm_ext import callProvider
    raw = callProvider(provider, EXTRACT_PROMPT + "\n\nTEXT:\n" + text, max_tokens=2000)
    out = []
    for line in raw.splitlines():
        parts = [p.strip() for p in line.split("|")]
        if len(parts) == 5:
            role, pred, f, c, src = parts
            try:
                out.append(Obs("mayorN", pred, min(0.99, float(f)), min(0.5, float(c)), role, src))
            except ValueError:
                continue
    return out


def load_atoms_metta(path: str):
    """Parse our data/*.metta atom files into Obs (provenance from trailing comment)."""
    obs = []
    pat = re.compile(r"\(\(-->\s+(\S+)\s+(\S+)\)\s+\(stv\s+([0-9.]+)\s+([0-9.]+)\)\)\s*;;\s*(\w+)?\s*(\[[^\]]*\])?")
    for line in open(path, encoding="utf-8"):
        m = pat.search(line)
        if m:
            subj, pred, f, c, role, src = m.groups()
            obs.append(Obs(subj, pred, float(f), float(c), role or "?", src or ""))
    return obs


# ===========================================================================
# PIPELINE
# ===========================================================================
def revise_axis(engine, atoms):
    """Fold revision over same-term atoms. Returns {term: (f,c), 'prov': [...]}."""
    by_term = {}
    for o in atoms:
        by_term.setdefault(o.term, []).append(o)
    merged = {}
    for term, group in by_term.items():
        tv = group[0].tv
        for o in group[1:]:
            tv = engine.revise2(term, tv, o.tv)
        merged[term] = {"tv": tv, "prov": [(o.role, o.src) for o in group]}
    return merged


def collide(engine, atoms, merged):
    """Axis B: plan a collision of STATED vs ENACTED-merged on each shared term."""
    tensions = []
    by_term = {}
    for o in atoms:
        by_term.setdefault(o.term, []).append(o)
    for term, group in by_term.items():
        stated = [o for o in group if o.role == "STATED"]
        enacted = [o for o in group if o.role == "ENACTED"]
        if not stated or not enacted:
            continue
        # ContextBridge = revise STATED vs ENACTED-merged
        e_tv = enacted[0].tv
        for o in enacted[1:]:
            e_tv = engine.revise2(term, e_tv, o.tv)
        bridged = engine.revise2(term, stated[0].tv, e_tv)
        f, c = bridged
        if c > 0.5 and NEAR_HALF[0] <= f <= NEAR_HALF[1]:
            token = "REJECT"
            tensions.append({"term": term, "tv": bridged, "token": token,
                             "prov": [(o.role, o.src) for o in group]})
    return tensions


def abduce_commitment(engine, atoms, commitments):
    """For an enacted behaviour, abduce the matching hidden commitment (c<=~0.45)."""
    subj = atoms[0].subj if atoms else "mayorN"   # all atoms share one subject
    # observed behaviour = strongest ENACTED behaviour atom set, revised
    by_pred = {}
    for o in atoms:
        if o.role == "ENACTED":
            by_pred.setdefault(o.pred, []).append(o)
    results = []
    for pred, group in by_pred.items():
        if pred not in commitments:
            continue
        tv = group[0].tv
        for o in group[1:]:
            tv = engine.revise2(f"(--> {subj} {pred})", tv, o.tv)
        commitment, rule_tv = commitments[pred]
        hyp = engine.abduce(commitment, pred, rule_tv, tv, subj)
        results.append({"commitment": commitment, "behaviour": pred,
                        "obs_tv": tv, "hyp": hyp, "subj": subj})
    return results


def load_commitments(path: str):
    """behaviour -> (commitment, (f,c)) from data/commitments.metta."""
    out = {}
    pat = re.compile(r"\(\(-->\s+(\S+)\s+(\S+)\)\s+\(stv\s+([0-9.]+)\s+([0-9.]+)\)\)")
    for line in open(path, encoding="utf-8"):
        m = pat.search(line)
        if m:
            commitment, behaviour, f, c = m.groups()
            out[behaviour] = (commitment, (float(f), float(c)))
    return out


def gate(tv):
    f, c = tv
    return "ACT" if GATE_ACT(f, c) else ("HYPOTHESIZE" if GATE_HYP(f, c) else "IGNORE")


def surface(tensions, abductions):
    """Pick the SHARPEST tension (distance of f from 0.5, weighted by c)."""
    if not tensions:
        return None
    sharp = max(tensions, key=lambda t: abs(0.5 - t["tv"][0]) * t["tv"][1])
    pred = sharp["term"].split()[-1].rstrip(")")
    hyp = next((a for a in abductions if _undermines(a, pred)), None)
    return {"tension": sharp, "abduction": hyp}


def _undermines(abduction, contested_pred):
    # crude mapping: takes-control undermines relies-on-team, etc. Driven by data.
    pairs = {"relies-on-team": "takes-control", "leads-openly": "withholds-vulnerability",
             "develops-others": "wont-delegate",
             # Raskolnikov benchmark
             "above-ordinary-morality": "acts-from-conscience",
             "self-sufficient-isolation": "seeks-human-communion"}
    return pairs.get(contested_pred) == abduction["behaviour"]


def receipt(s):
    t, hyp = s["tension"], s["abduction"]
    f, c = t["tv"]
    lines = [
        "— receipt —",
        f"tension term : {t['term']}",
        f"contested    : f={f:.2f} c={c:.2f}  ({t['token']})",
        f"supported by : {', '.join(src for _, src in t['prov'] if src)}",
    ]
    if hyp:
        hf, hc = hyp["hyp"]
        lines += [
            f"abduced      : (--> {hyp.get('subj', 'mayorN')} {hyp['commitment']})  f={hf:.2f} c={hc:.2f}",
            f"gate         : {gate(hyp['hyp'])}  (abduction is capped ~0.45 -> hypothesis)",
        ]
    return "\n".join(lines)


def surface_message(s):
    """Dosed insight + invitation (insight pacing). Never a label/number to the user."""
    t = s["tension"]
    pred = t["term"].split()[-1].rstrip(")")
    hyp = s["abduction"]
    msg = "I've been watching the last while, and something keeps showing up that you may not see in yourself.\n\n"
    if pred == "relies-on-team":
        msg += ("You value your team and mean it — but under pressure you keep taking the decision back. "
                "Maybe underneath sits a quiet commitment: \"to delegate is to risk what only I'll be blamed for.\" Does that land?")
    else:
        msg += f"Your stated stance and your actions pull apart around '{pred}'. Does that resonate?"
    return msg


# ===========================================================================
# ENTRY POINTS
# ===========================================================================
def _pipeline(engine, atoms, commitments):
    revise_axis(engine, atoms)                    # REVISE (per-term accumulation)
    tensions = collide(engine, atoms, None)       # COLLIDE (axis B) -> CONTESTED
    abductions = abduce_commitment(engine, atoms, commitments)  # ABDUCE -> hidden commitment
    s = surface(tensions, abductions)             # SURFACE (pick sharpest)
    if not s:
        return "IGNORE — nothing crossed threshold yet."
    return surface_message(s) + "\n\n" + receipt(s)


def run(text: str):
    """Live path: extract atoms from text, then run the pipeline."""
    engine = MirrorEngine()
    atoms = extract(text)
    commitments = load_commitments(os.path.join(DATA, "commitments.metta"))
    return _pipeline(engine, atoms, commitments)


def demo():
    """Reproducible path: pre-baked Mayor N atoms (reviewer runs this)."""
    engine = MirrorEngine()
    atoms = load_atoms_metta(os.path.join(DATA, "mayor_atoms.metta"))
    commitments = load_commitments(os.path.join(DATA, "commitments.metta"))
    return _pipeline(engine, atoms, commitments)


if __name__ == "__main__":
    print(demo())
