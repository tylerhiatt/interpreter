"""
TODO: Create a container class DatalogProgram to hold ->
A vector of Predicates for the schemes
A vector of Predicates for the facts
A vector of Predicates for the queries
A vector of Rules for the rules

Create a to_string() function

Each line needs 2 spaces
Count how many lines in each predicate
Include the Domain -> set of strings
"""

class DatalogProgram:
    def __init__(self, schemes, facts, queries, rules):
        self.schemes = schemes
        self.facts = facts
        self.queries = queries
        self.rules = rules

    def to_string(self):
        program_str = ""

        def format_predicate(predicate, end_symbol):
            return f"  {predicate.to_string()}{end_symbol}"
        
        def count_predicates(predicates):
            return len(predicates)

        # Convert and concatenate the schemes
        if self.schemes:
            program_str += f"Schemes({count_predicates(self.schemes)}):\n"
            program_str += "\n".join([format_predicate(scheme, '') for scheme in self.schemes])
            program_str += "\n"
        else:
            program_str += f"Schemes({count_predicates(self.schemes)}):\n"

        # Convert and concatenate the facts
        if self.facts:
            program_str += f"Facts({count_predicates(self.facts)}):\n"
            program_str += "\n".join([format_predicate(fact, '.') for fact in self.facts])
            program_str += "\n"
        else:
            program_str += f"Facts({count_predicates(self.facts)}):\n"

        # Convert and concatenate the rules
        if self.rules:
            program_str += f"Rules({count_predicates(self.rules)}):\n"
            program_str += "\n".join([format_predicate(rule, '.') for rule in self.rules])
            program_str += "\n"
        else:
            program_str += f"Rules({count_predicates(self.rules)}):\n"

        # Convert and concatenate the queries
        if self.queries:
            program_str += f"Queries({count_predicates(self.queries)}):\n"
            program_str += "\n".join([format_predicate(query, '?') for query in self.queries])
            program_str += "\n"
        else:
            program_str += f"Queries({count_predicates(self.queries)}):\n"

        # Domain
        domain = self.get_domain()
        program_str += "Domain(" + str(len(domain)) + "):\n"
        for item in domain:
            program_str += f"  {item}\n"

        return program_str
    
    def get_domain(self):
        # Collect unique string values from facts
        domain = set()
        for fact in self.facts:
            domain.update(fact.parameters)
        return sorted(domain)
    