# aka tuple class

class Row:
    def __init__(self, values: list[str]) -> None:
        self.values: list[str] = values
    
    def __eq__(self, other: 'Row') -> bool:
        return self.values == other.values

    def __hash__(self) -> int:
        return hash(tuple(self.values))
    
    def __lt__(self, other: 'Row') -> bool:
        return self.values < other.values
        