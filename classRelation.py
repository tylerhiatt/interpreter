from classHeader import Header
from classRow import Row

class Relation:
    def __init__(self, name: str, header: Header, rows: set = None) -> None:
        self.name: str = name
        self.header: Header = header
        if rows is None:
            self.rows: set[Row] = set()
        else:
            self.rows: set[Row] = rows

    def __str__(self) -> None:
        output_str: str = ""
        for row in sorted(self.rows):
            if len(row.values) == 0:
                continue  # got to next row, skips below code

            separator: str = ""
            output_str += "  "
            for i in range(len(self.header.values)):
                output_str += separator
                output_str += self.header.values[i]
                output_str += "="
                output_str += row.values[i]
                separator = ", "
            output_str += "\n"
        
        return output_str
    
    def add_row(self, row: Row) -> None:
        if len(row.values) != len(self.header.values):  
            raise ValueError("Row is not the same length as the header")
        
        self.rows.add(row)
    
    def select1(self, value: str, colIndex: int) -> 'Relation':

        if colIndex < 0 or colIndex >= len(self.header.values):
            raise ValueError(f"Column index {colIndex} is out of bounds")

        new_name = self.name + "_selected1"
        new_header = self.header
        new_rows = set()

        for row in self.rows:
            if row.values[colIndex] == value:
                new_rows.add(row)

        return Relation(new_name, new_header, new_rows)

    def select2(self, index1: int, index2: int) -> 'Relation':

        if index1 < 0 or index1 >= len(self.header.values) or index2 < 0 or index2 >= len(self.header.values):
            raise ValueError(f"One or both column indices ({index1}, {index2}) are out of bounds")

        new_name = self.name + "_selected2"
        new_header = self.header
        new_rows = set()

        for row in self.rows:
            if row.values[index1] == row.values[index2]:
                new_rows.add(row)

        return Relation(new_name, new_header, new_rows)
    
    def rename(self, new_header: Header) -> 'Relation':
        if len(new_header.values) != len(self.header.values):
            raise ValueError("New Header values must have the same number of columns as the old header")
        new_name = self.name + "_renamed"

        return Relation(new_name, new_header, self.rows)

    def project(self, col_indexes: list[int]) -> 'Relation':

        for index in col_indexes:
            if index < 0 or index >= len(self.header.values):
                raise ValueError(f"Column '{index}' does not exist in the original relation")
        
        new_header_values = [self.header.values[index] for index in col_indexes]
        final_header = Header(new_header_values)
        
        new_rows = set()
        for row in self.rows:
            new_row_values = [row.values[index] for index in col_indexes if 0 <= index < len(row.values)]
            new_rows.add(Row(new_row_values))
        
        new_name = self.name + "_projected"

        return Relation(new_name, final_header, new_rows)


    def can_join_rows(self, row1: Row, row2: Row, overlap: list[tuple[int,int]]) -> bool:
        for x, y in overlap:
            if row1.values[x] != row2.values[y]:
                return False
            
        return True
        
    def join_rows(self, row1: Row, row2: Row, unique_cols_1: list[int]) -> Row:
        new_row_values: list(str) = []
        for x in unique_cols_1:
            new_row_values.append(row1.values[x])

        # evaluate predicates should ensure that only unique values are considered
        new_row_values.extend(row2.values)

        return Row(new_row_values)
        
    
    def join_headers(self, header1: Header, header2: Header, unique_cols_1: list[int]) -> Header:
        new_header_values: list(str) = []
        for x in unique_cols_1:
            new_header_values.append(header1.values[x])

        new_header_values.extend(header2.values)

        return Header(new_header_values)


    def natural_join(self, other: 'Relation') -> 'Relation':
        r1: Relation = self
        r2: Relation = other
        
        overlap: list[tuple(int,int)] = []
        unique_cols_1: list[int] = []
        
        # step 1: calculate the correct values for overlap, and unique_cols_1
        for x in range(len(r1.header.values)):
            is_unique: bool = True
            for y in range(len(r2.header.values)):
                if r1.header.values[x] == r2.header.values[y]:
                    overlap.append(tuple([x, y]))
                    is_unique = False
            if is_unique:
                unique_cols_1.append(x)
                    
        # step 2: create new header
        h: Header = self.join_headers(r1.header, r2.header, unique_cols_1)

        # step 3: compare all rows and add rows together if possible
        result: Relation = Relation(r1.name + "|x|" + r2.name, h, set())
        for t1 in r1.rows:
            for t2 in r2.rows:
                if self.can_join_rows(t1, t2, overlap):
                    result_row = self.join_rows(t1, t2, unique_cols_1)
                    result.add_row(result_row)
        
        return result
    
    def union(self, other_relation: 'Relation') -> 'Relation':
        if len(self.header.values) != len(other_relation.header.values):
            raise ValueError("Relations are not union-compatible: different number of cols")
        
        combined_rows = self.rows.union(other_relation.rows)  # rows are represented as sets so

        new_name = f"{self.name}_union_{other_relation.name}"
        new_header = self.header

        return Relation(new_name, new_header, combined_rows)

 