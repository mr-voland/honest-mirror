;; ===========================================================================
;; raskolnikov_atoms.metta — atomised Raskolnikov (benchmark population)
;; ---------------------------------------------------------------------------
;; Source: Dostoevsky, "Crime and Punishment" (public domain). Atomised from key
;; scenes — NOT reproduced verbatim. Provenance tag in [brackets] after each atom.
;; Extraction rules (same as mayor_atoms.metta):
;;   - one pair ((--> subj pred) (stv f c)) per atom ; c <= 0.5 (LLM-overconfidence guard)
;;   - CONTRADICTION on ONE term: STATED theory vs ENACTED conduct, same predicate
;;   - ENACTED behaviours use the controlled vocabulary of commitments.metta so
;;     abduction can fire (acts-from-conscience)
;;
;; Ground-truth core (data/raskolnikov_ground_truth.md):
;;   primary tension  -> above-ordinary-morality  CONTESTED (f~0.36, c~0.77) REJECT
;;   abduced commitment -> bound-by-conscience (c~0.41, HYPOTHESIZE)
;;   secondary tension -> self-sufficient-isolation (weaker); SURFACE picks primary
;; ===========================================================================

;; ---- AXIS 1: theory of transgression <-> moral nature (PRIMARY, sharpest) ----

;; STATED — the article / the Porfiry conversation: the "extraordinary man" has the
;; right to step over moral law ("кровь по совести") for a higher idea.
((--> raskolnikov above-ordinary-morality)  (stv 0.85 0.45))   ;; STATED  [article-pravo-imeyu]

;; ENACTED — conduct that contradicts being "above morality" (same term -> revision -> CONTESTED)
((--> raskolnikov above-ordinary-morality)  (stv 0.15 0.45))   ;; ENACTED [marmeladov-last-money]
((--> raskolnikov above-ordinary-morality)  (stv 0.18 0.45))   ;; ENACTED [conscience-illness-after]
((--> raskolnikov above-ordinary-morality)  (stv 0.20 0.45))   ;; ENACTED [confession-yavka]

;; ENACTED — acts-from-conscience (same episodes) -> feeds abduction via commitments.metta
((--> raskolnikov acts-from-conscience)     (stv 0.85 0.45))   ;; ENACTED [marmeladov-last-money]
((--> raskolnikov acts-from-conscience)     (stv 0.82 0.45))   ;; ENACTED [conscience-illness-after]
((--> raskolnikov acts-from-conscience)     (stv 0.80 0.45))   ;; ENACTED [confession-yavka]
((--> raskolnikov acts-from-conscience)     (stv 0.80 0.45))   ;; ENACTED [drawn-to-sonya-faith]

;; ---- AXIS 2: self-sufficient isolation <-> need for the other (SECONDARY, weaker) ----

;; STATED — the "Napoleon" stands alone, needs no one, judges by himself
((--> raskolnikov self-sufficient-isolation) (stv 0.80 0.45))  ;; STATED  [napoleon-stands-alone]

;; ENACTED — against isolation (same term -> CONTESTED, fewer episodes)
((--> raskolnikov self-sufficient-isolation) (stv 0.25 0.45))  ;; ENACTED [reaches-for-sonya]
((--> raskolnikov self-sufficient-isolation) (stv 0.22 0.45))  ;; ENACTED [cannot-bear-alone]

;; ENACTED — seeks-human-communion -> abduction candidate (need-to-be-redeemed)
((--> raskolnikov seeks-human-communion)    (stv 0.78 0.45))   ;; ENACTED [reaches-for-sonya]
((--> raskolnikov seeks-human-communion)    (stv 0.75 0.45))   ;; ENACTED [cannot-bear-alone]

;; ---- COHERENT / uncontested STATED atoms (realism; should NOT surface) ----
((--> raskolnikov values-rationality)       (stv 0.88 0.45))   ;; STATED  [intellect-pride]
((--> raskolnikov despises-mediocrity)      (stv 0.82 0.45))   ;; STATED  [contempt-ordinary]
