"""
TODO:
Schemes, Facts, and Queries are just predicates
Rules are a way of creating relationships between predicates
A group of predicates (the body) can create new instances of a predicate (the head)

to_string() method
"""
from .class_parameter import Parameter

class Predicate:
    def __init__(self, name: str, parameters: list[str]):
        self.name = name
        # self.parameters = parameters
        self.parameters = [Parameter(param) for param in parameters]


    def to_string(self):
        param_str = ','.join(param.to_string() for param in self.parameters)
        return f"{self.name}({param_str})"