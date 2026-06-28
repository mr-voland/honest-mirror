;; ===========================================================================
;; skills.metta — registration fragment for The Honest Mirror
;; ---------------------------------------------------------------------------
;; How OmegaClaw exposes a skill (verified vs src/skills.metta):
;;   1) define a MeTTa function that dispatches to our Python module;
;;   2) add ONE description line to getSkills so the agent can call it.
;;
;; Install: copy skill/ into the OmegaClaw tree (or import this file), and add
;; the getSkills line below into src/skills.metta's getSkills list.
;; honest_mirror.py must be importable (PYTHONPATH or copied next to lib_llm_ext).
;; ===========================================================================

;; --- dispatch: agent command  honest-mirror "<text>"  -> Python orchestrator ---
(= (honest-mirror $text)
   (py-call (honest_mirror.run $text)))

;; --- reproducible demo command (pre-baked Mayor N) ---
(= (honest-mirror-demo)
   (py-call (honest_mirror.demo)))

;; --- ADD THIS LINE into the getSkills list in src/skills.metta: ---
;; "- Surface one value tension from reflection text as a hypothesis with receipt: honest-mirror string"
;; "- Run the reproducible Mayor N demo of the honest mirror: honest-mirror-demo"
