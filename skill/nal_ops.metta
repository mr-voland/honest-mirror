;; ===========================================================================
;; nal_ops.metta — thin helpers over the OmegaClaw NAL engine (lib_nal.metta)
;; ---------------------------------------------------------------------------
;; The heavy orchestration lives in honest_mirror.py (Python drives the loop,
;; the NAL ENGINE does the reasoning via |-). These are small, safe helpers
;; that can be called from MeTTa or mirrored in Python.
;;
;; Atom form (verified vs lib_nal.metta):  ((--> subj pred) (stv f c))
;; |- is BINARY:  (|- premiseA premiseB)
;; ===========================================================================

;; --- gate by NAL action thresholds ---
(= (gate (stv $f $c))
   (if (and (>= $f 0.6) (>= $c 0.5)) ACT
       (if (and (>= $f 0.3) (>= $c 0.2)) HYPOTHESIZE
           IGNORE)))

;; --- expectation: rank which tension is sharpest (distance of f from 0.5, weighted by c) ---
(= (expectation (stv $f $c)) (Truth_Expectation (stv $f $c)))

;; --- revision of two SAME-TERM atoms via the engine ---
;; |- on two same-term premises fires the revision |-nal rule:
;;   (|-nal ($T $T1) ($T $T2)) -> ($T (Truth_Revision $T1 $T2))
;; VERIFY in WSL: |- returns a superpose/collapse SET; in Python we pick the
;; member whose term == the shared input term. If calling from MeTTa directly,
;; Truth_Revision can be applied to the two truth-values on the matching term.
(= (revise2 ($T $tv1) ($T $tv2))
   ($T (Truth_Revision $tv1 $tv2)))

;; --- abduction: shared-predicate rule + observation -> hidden subject ---
;; (|-nal ((--> $a $c) $T1) ((--> $b $c) $T2)) -> ((--> $b $a) (Truth_Abduction $T1 $T2))
;; VERIFY in WSL: run via (|- $rule $observed) and pick the ((--> $b $a) _) member.
(= (abduce-hidden ((--> $a $c) $T1) ((--> $b $c) $T2))
   ((--> $b $a) (Truth_Abduction $T1 $T2)))
