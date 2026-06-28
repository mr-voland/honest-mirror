;; ===========================================================================
;; mayor_atoms.metta — atomised Mayor N (demo population)
;; ---------------------------------------------------------------------------
;; Source: data/mayor_source.md  (provenance tag in [brackets] after each atom)
;; Extraction rules honoured:
;;   - one pair  ((--> subj pred) (stv f c))  per atom
;;   - c <= 0.5 (LLM over-confidence guard)
;;   - CONTRADICTION lives on ONE term: STATED vs ENACTED truths on same predicate
;;   - ENACTED behaviours use the controlled vocabulary of commitments.metta so
;;     abduction can fire (takes-control / withholds-vulnerability)
;;   - provenance (STATED/ENACTED + source) is metadata here, NOT inside the atom
;;
;; Expected surface (ground truth for this demo):
;;   primary tension  -> relies-on-team  CONTESTED (f~0.4, c high) over 3 episodes
;;   abduced commitment -> protect-sole-accountability (c~0.45, HYPOTHESIZE)
;;   secondary tension -> leads-openly CONTESTED (weaker, 2 episodes); SURFACE picks primary
;; ===========================================================================

;; ---- AXIS 1: control <-> trust  (PRIMARY, sharpest) ----------------------

;; STATED (interview 1) — self-presentation, c moderate
((--> mayorN relies-on-team)         (stv 0.90 0.45))   ;; STATED  [i1-team]

;; ENACTED — evidence AGAINST relies-on-team (same term -> revision -> CONTESTED)
((--> mayorN relies-on-team)         (stv 0.15 0.45))   ;; ENACTED [i2-budget]
((--> mayorN relies-on-team)         (stv 0.18 0.45))   ;; ENACTED [i2-failed]
((--> mayorN relies-on-team)         (stv 0.20 0.45))   ;; ENACTED [n-control2]

;; ENACTED — takes-control (same episodes) -> feeds abduction via commitments.metta
((--> mayorN takes-control)          (stv 0.85 0.45))   ;; ENACTED [i2-budget]
((--> mayorN takes-control)          (stv 0.82 0.45))   ;; ENACTED [i2-failed]
((--> mayorN takes-control)          (stv 0.80 0.45))   ;; ENACTED [n-control1]
((--> mayorN takes-control)          (stv 0.80 0.45))   ;; ENACTED [n-control3]

;; ---- AXIS 2: openness <-> self-protection  (SECONDARY, weaker) -----------

;; STATED (interview 1)
((--> mayorN leads-openly)           (stv 0.80 0.45))   ;; STATED  [i1-open]

;; ENACTED — against leads-openly (same term -> CONTESTED, fewer episodes)
((--> mayorN leads-openly)           (stv 0.25 0.45))   ;; ENACTED [n-weak1]
((--> mayorN leads-openly)           (stv 0.22 0.45))   ;; ENACTED [n-weak2]

;; ENACTED — withholds-vulnerability -> abduction candidate (avoid-exposure-of-weakness)
((--> mayorN withholds-vulnerability)(stv 0.78 0.45))   ;; ENACTED [n-weak1]
((--> mayorN withholds-vulnerability)(stv 0.75 0.45))   ;; ENACTED [n-weak2]

;; ---- COHERENT / uncontested STATED atoms (realism; should NOT surface) ----
((--> mayorN listens-to-citizens)    (stv 0.88 0.45))   ;; STATED  [i1-listen]
((--> mayorN develops-others)        (stv 0.85 0.45))   ;; STATED  [i1-develop]
