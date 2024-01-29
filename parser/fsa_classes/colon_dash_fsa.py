from .fsa import FSA
from typing import Callable

class ColonDashFSA(FSA):
    def __init__(self) -> None:
        FSA.__init__(self, "COLON_DASH") 
        self.accept_states.add(self.S2)

    def S0(self) -> Callable:
        current_input: str = self._FSA__get_current_input()
        next_state: Callable = None
        if current_input == ':': 
            next_state = self.S1
        else: 
            next_state = self.S_err
            self.error = True
        return next_state

    def S1(self) -> Callable:
        current_input: str = self._FSA__get_current_input()
        next_state: Callable = None
        if current_input == '-': 
            next_state = self.S2
            self.accepted = True
        else: 
            next_state = self.S_err
            self.error = True
        return next_state

    def S2(self) -> Callable:
        current_input: str = self._FSA__get_current_input()
        next_state: Callable = self.S2 # loop in state s2
        return next_state

    def S_err(self) -> Callable:
        current_input: str = self._FSA__get_current_input()
        next_state: Callable = self.S_err # loop in state s_err
        return next_state