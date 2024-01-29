"""
TODO:
A parameter can be a STRING or an ID
A STRING has ' ' around it (ex. '5')
An ID does not have ' ' around it (ex. Y)
STRING and ID are just textual values

to_string() method
"""

class Parameter:
    def __init__(self, value: str):
        self.value = value
        # assume that if value starts with a quote, it's a constant, otherwise it's a variable
        self.is_constant = value.startswith("'") and value.endswith("'")

    def __eq__(self, other: 'Parameter') -> bool:
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(tuple(self.value))
    
    def __lt__(self, other: 'Parameter') -> bool:
        return self.value < other.value

    def get_value(self):
        # return self.value.strip("'") if self.is_constant else self.value
        return self.value

    def to_string(self):
        return self.value
