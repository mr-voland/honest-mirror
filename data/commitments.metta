;; ===========================================================================
;; commitments.metta — competing-commitment library (Immunity to Change)
;; ---------------------------------------------------------------------------
;; Seeded as BACKGROUND knowledge each cycle. Generic, open ITC theory only —
;; Generic, open Immunity-to-Change theory only — no proprietary lenses or third-party material.
;;
;; Form:  ((--> <hidden-commitment> <behaviour>) (stv f c))
;;   Read as: "the hidden commitment manifests as this behaviour."
;;
;; Abduction rule fires on a SHARED predicate <behaviour>:
;;   premise A (library):   ((--> <commitment> <behaviour>) (stv 1.0 0.9))
;;   premise B (observed):  ((--> mayorN     <behaviour>) (stv 0.85 0.70))
;;   => conclusion:         ((--> mayorN <commitment>)   (stv 0.85 ~0.45))  -> HYPOTHESIZE
;;
;; The engine SELECTS the commitment whose behaviour matches the observed
;; enacted pole — it is not hard-coded to one answer.
;; ===========================================================================

;; commitment                          behaviour                    undermines stated value
((--> protect-sole-accountability takes-control)           (stv 1.0 0.9))   ;; "I rely on my team"
((--> avoid-exposure-of-weakness  withholds-vulnerability)  (stv 1.0 0.9))   ;; "I lead openly"
((--> need-to-be-indispensable    wont-delegate)            (stv 1.0 0.9))   ;; "I develop others"
((--> preserve-being-right        resists-dissent)          (stv 1.0 0.9))   ;; "I want to be challenged"
((--> avoid-conflict              defers-hard-decisions)    (stv 1.0 0.9))   ;; "I am decisive"

;; --- Raskolnikov benchmark commitments (generic ITC framing, public-domain character) ---
((--> bound-by-conscience         acts-from-conscience)     (stv 1.0 0.9))   ;; "I am above ordinary morality"
((--> need-to-be-redeemed         seeks-human-communion)    (stv 1.0 0.9))   ;; "I am self-sufficient, need no one"
