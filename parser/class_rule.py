"""
TODO:
Rules are a way of creating relationships between predicates
A group of predicates (the body) can create new instances of a predicate (the head)

to_string() method
"""

class Rule:
    def __init__(self, head, body_predicates):
        self.head = head
        self.body_predicates = body_predicates

    def to_string(self):
        body_str = ','.join([pred.to_string() for pred in self.body_predicates])
        return f"{self.head.to_string()} :- {body_str}"