import sys
sys.path.append("/PeTTa/python")
from petta import PeTTa

class MeTTa:
    def __init__(self):
        self._petta = PeTTa()
        
    def run(self, code_str: str):
        # Prolog petta.py requires compiling definitions and runnables.
        # process_metta_string compiles definitions and executes !(...) expressions.
        return self._petta.process_metta_string(code_str)
