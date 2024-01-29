from classRelation import Relation
from classRow import Row
from classHeader import Header
from typing import Dict

from parser.my_parser import Parser
from parser.class_parameter import Parameter
from parser.class_datalog_program import DatalogProgram
from parser.class_predicate import Predicate
from parser.class_rule import Rule
from classGraph import Graph


class Interpreter:
    def __init__(self) -> None:
        self.output_str: str = ""
        self.database: Dict[str, Relation] = {}
    
    def run(self, datalog_program: DatalogProgram) -> str:
        self.datalog_program: DatalogProgram = datalog_program
        self.interpret_schemes()
        self.interpret_facts()
        self.interpret_rules() 
        self.interpret_queries()
        return self.output_str
    
    def interpret_schemes(self) -> None:
        # Start with an empty Database. 
        self.database: Dict[str, Relation] = {}

        for scheme in self.datalog_program.schemes:
            header = Header([parameter.to_string() for parameter in scheme.parameters])
            relation = Relation(scheme.name, header)
            self.database[relation.name] = relation


    def interpret_facts(self) -> None:
        # For each fact in the Datalog program, add a tuple to the relation.
        for fact in self.datalog_program.facts:
            # Use the predicate name from the fact to 
            # determine the Relation to which the Tuple should be added. 
            relation_name = fact.name
            # if relation doesn't exist, there is an error
            if relation_name not in self.database:
                raise ValueError(f"No relation found for predicate name: {relation_name}")
        
            # Use the values listed in the fact to provide the values for the Tuple.
            relation = self.database[relation_name]
            row = Row([parameter.get_value() for parameter in fact.parameters])

            relation.add_row(row)

    
    def interpret_queries(self) -> None:
        self.output_str += "\nQuery Evaluation\n"

        for query in self.datalog_program.queries:
            result = self.evaluate_predicate(query)
            
            # For each query, output the query and a space. 
            self.output_str += f"{query.to_string()}? "

            if not result.rows:
                self.output_str += "No\n"
            else:
                self.output_str += f"Yes({(len(result.rows))})\n"

                # Output the tuples in sorted order. 
                # Sort the tuples alphabetically based on the values in the tuples. 
                # Sort first by the value in the first position and if needed up to the value in the nth position.
                if any(not param.is_constant for param in query.parameters):
                    sorted_rows = sorted(result.rows, key = lambda row: row.values)
                    for row in sorted_rows:
                        self.output_str += "  "  # indent the output
                        pairs = [f"{name}={value}" for name, value in zip(result.header.values, row.values)]
                        self.output_str += ", ".join(pairs) + "\n"
                

    def evaluate_predicate(self, predicate: Predicate) -> Relation:
        relation = self.database[predicate.name]

        variables_pos = {}
        constant_vals = {}

        for i, param in enumerate(predicate.parameters):
            if param.is_constant:  # check if the parameter is a constant
                constant_vals[i] = param.get_value()
            else:
                # it's a variable, record the first position of each variable
                variables_pos[param.get_value()] = variables_pos.get(param.get_value(), i)

        # Perform selections for constants
        for position, value in constant_vals.items():
            relation = relation.select1(value, position)

        # Perform selections for matching variables
        for variable, position in variables_pos.items():
            for i, param in enumerate(predicate.parameters):
                if i > position and param.get_value() == variable:
                    relation = relation.select2(position, i)

        project_columns = sorted(set(variables_pos.values()))
        relation = relation.project(project_columns)
        # relation = relation.project([relation.header.values[i] for i in project_columns])

        rename_header_values = [predicate.parameters[i].to_string() for i in project_columns]
        relation = relation.rename(Header(rename_header_values))

        # The operations must be done in the order described above: 
        #   any selects, 
        #   followed by a project, 
        #   followed by a rename.
        # return the new predicate
        return relation
    
    def interpret_rules(self) -> None:
        # get the rules from datalog and show the dependency graph
        graph = Graph()
        graph.populate(self.datalog_program.rules)
        self.output_str += graph.graph_to_string() + "\n"

        self.output_str += "Rule Evaluation\n"

        # get the post order and sccs
        post_order = graph.dfs_forest_reverse()
        sccs = graph.dfs_forest_scc(post_order)

        # evaluate rules within each SCC
        for scc in sccs:
            sorted_scc = sorted(list(scc))
            self.output_str += f"SCC: {','.join(['R' + str(rule_index) for rule_index in sorted_scc])}\n"
            
            if len(sorted_scc) == 1 and sorted_scc[0] not in graph.forward_graph[sorted_scc[0]]:
                rule_index = sorted_scc[0]
                rule = self.datalog_program.rules[rule_index]
                new_tuples = self.evaluate_rule(rule)
                self.output_str += f"{rule.to_string()}.\n"
                for tup in new_tuples:
                    self.output_str += f"  {tup}\n"
                self.output_str += f"1 passes: R{str(rule_index)}\n"
            else:
                passes = 0
                new_tuples_added = True
                while new_tuples_added:
                    new_tuples_added = False
                    for rule_index in scc:
                        rule = self.datalog_program.rules[rule_index]
                        new_tuples = self.evaluate_rule(rule)
                        self.output_str += f"{rule.to_string()}.\n"

                        if new_tuples:
                            # self.output_str += f"{rule.to_string()}.\n"
                            for tup in new_tuples:
                                self.output_str += f"  {tup}\n"
                            new_tuples_added = True
                    passes += 1
                
                self.output_str += f"{passes} passes: {','.join(['R' + str(rule_index) for rule_index in sorted_scc])}\n"
                # self.output_str += f"{passes} passes: R{str(scc.pop())}\n"
    
    # this function should return the number of unique tuples added to the database
    def evaluate_rule(self, rule: Rule) -> int:
        # Step 1:   
        # Evaluate the predicates on the right-hand side of the rule (the body predicates):
        intermediate_relations = []
        for body_predicate in rule.body_predicates:
            result = self.evaluate_predicate(body_predicate)
            intermediate_relations.append(result)

        # Step 2:
        # If there are two or more predicates on the right-hand side of a rule, 
        #   join the intermediate results to form the single result for Step 2. 
        if len(intermediate_relations) > 1:
            joined_relation = intermediate_relations[0]  # grab the first element in intermediate_relations
            for relation in intermediate_relations[1:]:
                joined_relation = joined_relation.natural_join(relation)
                # print(f"Type of joined_relation: {type(joined_relation)}") 

        # If there is a single predicate on the right hand side of the rule, 
        #   use the single intermediate result from Step 1 as the result for Step 2.
        else:
            joined_relation = intermediate_relations[0]

        # Step 3:
        # Project the columns that appear in the head predicate:
        head_predicate = rule.head
        project_columns = []
        for param in head_predicate.parameters:
            if param.get_value() in joined_relation.header.values:
                position = joined_relation.header.values.index(param.get_value())
                project_columns.append(position)

        projected_relation = joined_relation.project(project_columns)

        # Step 4:
        # Rename the relation to make it union-compatible:
        rename_header_values = [param.get_value() for param in head_predicate.parameters]
        renamed_relation = projected_relation.rename(Header(rename_header_values))

        # Step 5:
        # Union with the relation in the database:
        database_relation = self.database[head_predicate.name]
        #size_before = len(database_relation.rows)
        new_rows = renamed_relation.rows.difference(database_relation.rows)
        database_relation.rows = database_relation.rows.union(renamed_relation.rows)
        #size_after = len(database_relation.rows)
        # return size_after - size_before

        # only return rows that were added
        new_rows_as_strings = [self.row_to_string(row, database_relation.header) for row in sorted(new_rows)]
        database_relation.rows.update(new_rows)
        return new_rows_as_strings
    


    def row_to_string(self, row: Row, header: Header) -> str:
        row_values = []
        for i, value in enumerate(row.values):
            # value is a string, not a predicate
            value_str = value
            # Convert the attribute names to lowercase
            attribute_name = header.values[i]
            row_values.append(f"{attribute_name}={value_str}")
        return ", ".join(row_values)



