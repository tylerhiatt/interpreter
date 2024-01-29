from .fsa import FSA
from typing import Callable
from string import punctuation

class StringFSA(FSA):
    def __init__(self) -> None:
        FSA.__init__(self, "STRING")
        self.accept_states.add(self.S2)

    def run(self, input_string: str) -> bool:
        self.input_string = input_string
        current_state: Callable = self.start_state

        while self.num_chars_read < len(self.input_string):
            current_state = current_state()

            #ID FSA BREAK
            if self.accepted and (self.input_string[self.num_chars_read].isspace() or self.input_string[self.num_chars_read] in punctuation):
                break

        if current_state in self.accept_states:
            self.accepted = True
            return self.accepted
        
        return self.accepted
    
    
    def S0(self):
        current_input: str = self._FSA__get_current_input()
        next_state: Callable = None
        if current_input == '\'': 
            next_state = self.S1
        else: 
            next_state = self.S_err
            self.error = True
        return next_state
    
    def S1(self):
        current_input: str = self._FSA__get_current_input()
        next_state: Callable = None
        if current_input != '\'': 
            next_state = self.S1
        elif current_input is None:
            next_state = self.S_err
            self.error = True
        else: 
            next_state = self.S2
            self.accepted = True
        return next_state
    
    def S2(self):
        current_input: str = self._FSA__get_current_input()
        next_state: Callable = self.S2
        return next_state
    
        
    def S_err(self):
        current_input: str = self._FSA__get_current_input()
        next_state: Callable = self.S_err
        return next_state
