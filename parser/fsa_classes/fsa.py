from typing import Callable

class FSA:
    def __init__(self, name: str) -> None:
        self.start_state: function = self.S0
        self.accept_states: set[Callable] = set()

        self.input_string: str = ""
        self.fsa_name: str = name
        self.num_chars_read: int = 0

        self.accepted = False
        self.error = False
    
    def S0(self) -> NotImplemented:
        pass
    
    def run(self, input_string: str) -> bool:
        self.input_string = input_string
        current_state: Callable = self.start_state

        while self.num_chars_read < len(self.input_string):
            current_state = current_state()  # Call the current state function

            if self.accepted:
                break
        
        # check whether FSA ended in an accept state
        if current_state in self.accept_states: 
            self.accepted = True
            return self.accepted
        
        return self.accepted

    def reset(self) -> None:
        self.num_chars_read = 0
        # self.input_string = ""
        self.accepted = False
        self.error = False
        self.start_state = self.S0

    def get_name(self) -> str: 
        return self.fsa_name

    def set_name(self, FSA_name) -> None:
        self.fsa_name = FSA_name

    # def get_num_read(self) -> int:
    #     return self.num_chars_read

    # def get_new_lines(self) -> int:
    #     return self.new_lines

    def __get_current_input(self) -> str:  # private method
        current_input: str = self.input_string[self.num_chars_read]
        self.num_chars_read += 1
        # if current_input == '\n':
        #     self.new_lines += 1  # Track new lines
        return current_input