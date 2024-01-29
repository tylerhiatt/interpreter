from parser.class_rule import Rule

class Graph:
    def __init__(self) -> None:
        self.forward_graph: dict[int, set[int]] = {}
        self.reverse_graph: dict[int, set[int]] = {}

    def populate(self, rules: list[Rule]) -> None:
        for i in range(len(rules)):
            self.forward_graph[i] = set()
            self.reverse_graph[i] = set()

        for rule_from_index, rule_from in enumerate(rules):
            for body in rule_from.body_predicates:
                for rule_to_index, rule_to in enumerate(rules):
                    if body.name == rule_to.head.name:
                        self.forward_graph[rule_from_index].add(rule_to_index)
                        self.reverse_graph[rule_to_index].add(rule_from_index)
    
    def graph_to_string(self) -> str:
        output: str = "Dependency Graph\n"
        for i in range(len(self.forward_graph)):
            output += f"R{str(i)}:"
            dependencies = [f"R{str(j)}" for j in self.forward_graph[i]]
            output += ','.join(dependencies)
            output += "\n"
        return output
    
    def dfs_for_reverse(self, node: int, visited: set[int], post_order: list[int]) -> None:
        visited.add(node)
        for neighbor in self.reverse_graph[node]:
            if neighbor not in visited:
                self.dfs_for_reverse(neighbor, visited, post_order)
        post_order.append(node)

    def dfs_for_scc(self, node: int, visited: set[int], current_scc: set[int]) -> None:
        visited.add(node)
        current_scc.add(node)
        for neighbor in self.forward_graph[node]:
            if neighbor not in visited:
                self.dfs_for_scc(neighbor, visited, current_scc)

    def dfs_forest_reverse(self) -> list[int]:
        visited = set()
        post_order_list = []
        for node in range(len(self.reverse_graph)):
            if node not in visited:
                self.dfs_for_reverse(node, visited, post_order_list)
        return post_order_list[::-1]  # gets post order by reversing list
    
    def dfs_forest_scc(self, post_order: list[int]) -> list[set[int]]:
        visited = set()
        scc_list = []
        for node in post_order:
            if node not in visited:
                current_scc = set()
                self.dfs_for_scc(node, visited, current_scc)
                scc_list.append(current_scc)
        return scc_list


# testing
# rules = [Rule("s", ["s"]),
#          Rule("a", ["a", "p"]),
#          Rule("a", ["p"])]

# g = Graph()
# g.populate(rules)
# print(g.graph_to_string())