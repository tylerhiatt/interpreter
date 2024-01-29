from .fsa import FSA
from typing import Callable

class PeriodFSA(FSA):
    def __init__(self) -> None:
        FSA.__init__(self, "PERIOD")
        self.accept_states.add(self.S1)

    def S0(self):
        current_input: str = self._FSA__get_current_input()
        next_state: Callable = None
        if current_input == '.': 
            next_state = self.S1
            self.accepted = True
        else: 
            next_state = self.S_err
            self.error = True    
        return next_state
    
    def S1(self):
        current_input: str = self._FSA__get_current_input()
        next_state: Callable = self.S1
        return next_state
    
    def S_err(self):
        current_input: str = self._FSA__get_current_input()
        next_state: Callable = self.S_err
        return next_state