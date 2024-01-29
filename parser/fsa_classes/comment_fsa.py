from .fsa import FSA
from typing import Callable

class CommentFSA(FSA):
    def __init__(self) -> None:
        FSA.__init__(self, "COMMENT")
        self.accept_states.add(self.S1)
    
    
    # Change the inherited run method for comment case
    def run(self, input_string: str) -> bool:
        self.input_string = input_string
        current_state: Callable = self.start_state

        while self.num_chars_read < len(self.input_string):
            current_state = current_state()

            # if it's both accepted and the string is the end of the current line
            if self.accepted and self.input_string[self.num_chars_read] == '\n':
                break

        # check whether FSA ended in an accept state
        if current_state in self.accept_states: 
            self.accepted = True
            return self.accepted
        
        return self.accepted
    
    
    def S0(self):
        current_input: str = self._FSA__get_current_input()
        next_state: Callable = None
        if current_input == '#': 
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