from .fsa import FSA
from typing import Callable

class LeftParenFSA(FSA):
    def __init__(self):
        FSA.__init__(self, "LEFT_PAREN") 
        self.accept_states.add(self.S1) 
    
    def S0(self):
        current_input: str = self._FSA__get_current_input()
        next_state: Callable = None
        if current_input == '(': 
            next_state = self.S1
            self.accepted = True
        else: 
            next_state = self.S_err
            self.error = True
        return next_state

    def S1(self):
        current_input: str = self._FSA__get_current_input()
        next_state: Callable = self.S1 # loop in state s1
        return next_state
    
    def S_err(self):
        current_input: str = self._FSA__get_current_input()
        next_state: Callable = self.S_err # loop in state s_err
        return next_state