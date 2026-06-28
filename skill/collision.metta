;; ===========================================================================
;; collision.metta — forced cross-context collision (Axis B)
;; ---------------------------------------------------------------------------
;; "Self-opacity structurally expensive" (Goertzel, Theorem 5). The pipeline
;; does NOT wait to notice a contradiction — an AuditTask PLANS the collision
;; of two compartments (a STATED-source claim vs an ENACTED-source claim on the
;; SAME term), bridges them via cross-context NAL revision, and a CollisionToken
;; renders the verdict. REJECT raises a TENSION node.
;;
;; Conceptual type vocabulary (used in the receipt). The working verdict logic
;; runs in honest_mirror.py (Python), operating on the |- bridge result; these
;; definitions document the contract and give the receipt its vocabulary.
;; ===========================================================================

;; AuditTask: a planned pairing of two compartments on a shared term.
;;   (AuditTask <term> <stated-atom> <enacted-merged-atom>)

;; ContextBridge = cross-context NAL revision of the two compartments.
;;   (ContextBridge <stated-atom> <enacted-atom>)  ==  (|- <stated> <enacted>)

;; CollisionToken verdict from the bridged truth-value:
;;   REJECT     — claims cancel (f in near-half band) with non-trivial c  -> raise TENSION
;;   QUARANTINE — ambiguous (low c)                                       -> keep, gather more
;;   ADMIT      — claims agree (f far from 0.5, decent c)                 -> coherent, no tension
;; near-half band is a RANGE (not the point 0.5): behaviour can outweigh speech,
;; so a real contradiction often lands ~0.35 rather than exactly 0.5.
(= (collision-token (stv $f $c))
   (if (and (> $c 0.5) (and (>= $f 0.30) (<= $f 0.70))) REJECT
       (if (< $c 0.35) QUARANTINE
           ADMIT)))
