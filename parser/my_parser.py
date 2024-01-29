"""
TODO: Parser class ->
Takes in Token objects from lexer output
Checks the syntax
Run this to see if you get "Success!" or "Failure!" appropriately for the tests on the website

Modify class to create instances of DatalogProgram classes

NOTES:
- make a function for each non-terminal in the grammar
- inside that function, for a terminal, call self.match(), for a nonterminal call the corresponding function
- inside the parse() function call the function for the start symbol (funciton in notebook is parse_input())
- handle multiple productions with conditionality,use FIRST and/or FOLLOW set to determine whether to continue recursion or terminate it

"""
from .my_token import Token
from .class_predicate import Predicate
from .class_rule import Rule
from .class_datalog_program import DatalogProgram

class Parser():
    """ GRAMMAR for the Project:
    datalogProgram	->	SCHEMES COLON scheme schemeList FACTS COLON factList RULES COLON ruleList QUERIES COLON query queryList EOF

    schemeList	->	scheme schemeList | lambda
    factList	->	fact factList | lambda
    ruleList	->	rule ruleList | lambda
    queryList	->	query queryList | lambda

    scheme   	-> 	ID LEFT_PAREN ID idList RIGHT_PAREN
    fact    	->	ID LEFT_PAREN STRING stringList RIGHT_PAREN PERIOD
    rule    	->	headPredicate COLON_DASH predicate predicateList PERIOD
    query	        ->      predicate Q_MARK

    headPredicate	->	ID LEFT_PAREN ID idList RIGHT_PAREN
    predicate	->	ID LEFT_PAREN parameter parameterList RIGHT_PAREN
        
    predicateList	->	COMMA predicate predicateList | lambda
    parameterList	-> 	COMMA parameter parameterList | lambda
    stringList	-> 	COMMA STRING stringList | lambda
    idList  	-> 	COMMA ID idList | lambda
    parameter	->	STRING | ID
    """

    def __init__(self):
        # self.index = 0
        # self.tokens = []
        ...

    ### helper functions needed ##############################################################
    def get_curr_token(self) -> Token:
        # protection against going outside of index
        if (self.index >= len(self.tokens)):
            self.index = len(self.tokens) - 1
            self.throw_error()
        return self.tokens[self.index]
    
    def get_prev_token_val(self) -> str:
        return self.tokens[self.index - 1].value

    def throw_error(self):
        raise ValueError(self.get_curr_token().to_string())
        
    def advance(self):
        # move to the next token
        self.index += 1

    def match(self, expected_type: str):
        # __current_input_matches_target() function from jupyter notebook
        # checks if the next token has the provided type, if so, advance to the next token, else throw an error
        if (self.get_curr_token().token_type == expected_type):
            self.advance()
        else:
            self.throw_error()

    def run(self, tokens: list[Token]) -> str:
        self.index: int = 0
        self.tokens: list[Token] = tokens

        try:
            # call datalog_program function to call whole program, call specific functions to test
            datalog_program: DatalogProgram = self.datalog_program()
            # self.datalog_program()
            # return "Success!\n" + datalog_program.to_string()
            # print("Success!\n" + datalog_program.to_string())
            return datalog_program
        except ValueError as error_msg:
            return f"Failure!\n  {error_msg}"


    ### Call each non-terminal and apply its grammar needed ########################################
    def datalog_program(self):
        """datalogProgram -> SCHEMES COLON scheme schemeList 
                             FACTS COLON factList RULES COLON 
                             ruleList QUERIES COLON query queryList EOF
        """
        self.match("SCHEMES")
        self.match("COLON")
        schemes = [self.scheme()]
        schemes += self.scheme_list()
        self.match("FACTS")
        self.match("COLON")
        facts = self.fact_list()
        self.match("RULES")
        self.match("COLON")
        rules = self.rule_list()
        self.match("QUERIES")
        self.match("COLON")
        queries = [self.query()]
        queries += self.query_list()
        self.match("EOF")

        return DatalogProgram(schemes, facts, queries, rules)

    ### SCHEME PRODUCTIONS #########################################################################

    def scheme(self) -> Predicate:
        """scheme -> ID LEFT_PAREN ID idList RIGHT_PAREN
        """
        # define variables for predicate object
        name = ""
        parameters: list[str] = []

        # run through production
        self.match("ID")
        name = self.get_prev_token_val()
        self.match("LEFT_PAREN")
        self.match("ID")
        parameters.append(self.get_prev_token_val())
        parameters += self.id_list()
        self.match("RIGHT_PAREN")  # handles FOLLOW set
        return Predicate(name, parameters)
    
    def id_list(self) -> list[str]:
        """ idList -> COMMA ID idList | lambda
        """
        # Production 1
        if (self.get_curr_token().token_type == "COMMA"):
            self.match("COMMA")
            self.match("ID")
            current_id: list[str] = [self.get_prev_token_val()]
            rest_ids: list[str] = self.id_list()
            return current_id + rest_ids
        
        # Production 2 
        else:
            return []
        
    ### FACT PRODUCTIONS #########################################################################

    def fact(self) -> Predicate:
        """fact -> ID LEFT_PAREN STRING stringList RIGHT_PAREN PERIOD 
        """
        # define variables for predicate object
        name: str = ""
        parameters: list[str] = []

        # run through the production
        self.match("ID")
        name = self.get_prev_token_val()
        self.match("LEFT_PAREN")
        self.match("STRING")
        parameters.append(self.get_prev_token_val())
        parameters += self.string_list()
        # self.string_list()
        self.match("RIGHT_PAREN")
        self.match("PERIOD")
        return Predicate(name, parameters)
    
    def string_list(self) -> list[str]:
        """stringList -> COMMA STRING stringList | lambda
        """
        # Production 1
        if self.get_curr_token().token_type == "COMMA":
            self.match("COMMA")
            self.match("STRING")
            current_id: list[str] = [self.get_prev_token_val()]
            rest_ids: list[str] = self.string_list()
            # self.string_list()
            return current_id + rest_ids

        # Production 2
        else:
            return []
        
    ### RULE PRODUCTIONS #########################################################################

    def rule(self):
        """rule -> headPredicate COLON_DASH predicate predicateList PERIOD 
        """
        head = self.head_predicate()
        self.match("COLON_DASH")
        body_pred = self.predicate()
        body_pred_list = self.predicate_list()
        self.match("PERIOD")
        return Rule(head, [body_pred] + body_pred_list)

    def head_predicate(self):
        """headPredicate ->	ID LEFT_PAREN ID idList RIGHT_PAREN
        """
        self.match("ID")
        name = self.get_prev_token_val()
        self.match("LEFT_PAREN")
        self.match("ID")
        parameters = [self.get_prev_token_val()] + self.id_list()
        #self.id_list()
        self.match("RIGHT_PAREN")
        return Predicate(name, parameters)

    def predicate(self):
        """predicate ->	ID LEFT_PAREN parameter parameterList RIGHT_PAREN
        """
        # define variables for predicate object
        name = ""
        parameters: list[str] = []

        self.match("ID")
        name = self.get_prev_token_val()
        self.match("LEFT_PAREN")
        parameter = self.parameter()
        parameter_list = self.parameter_list()
        self.match("RIGHT_PAREN")

        parameters = [parameter] + parameter_list if parameter else parameter_list
        return Predicate(name, parameters)

    def predicate_list(self):
        """predicateList ->	COMMA predicate predicateList | lambda
        """
        # Production 1
        if self.get_curr_token().token_type == "COMMA":
            self.match("COMMA")
            predicate = self.predicate()
            predicate_list = self.predicate_list()
            if predicate:
                return [predicate] + predicate_list
            else:
                return predicate_list

        # Production 2
        else:
            return []
    
    def parameter(self):
        """parameter ->	STRING | ID
        """
        if self.get_curr_token().token_type == "STRING":
            self.match("STRING")
            string_val = self.get_prev_token_val()
            return string_val
        elif self.get_curr_token().token_type == "ID":
            self.match("ID")
            id_val = self.get_prev_token_val()
            return id_val
        else:
            self.throw_error()
    
    def parameter_list(self):
        """parameterList -> COMMA parameter parameterList | lambda
        """
        # Production 1
        if self.get_curr_token().token_type == "COMMA":
            self.match("COMMA")
            parameter = self.parameter()
            parameter_list = self.parameter_list()
            if parameter:
                return [parameter] + parameter_list
            else:
                return parameter_list
    
        # Production 2
        else:
            return []

    ### QUERY PRODUCTIONS #########################################################################

    def query(self) -> Predicate:
        """query -> predicate Q_MARK 
        """
        predicate = self.predicate()
        self.match("Q_MARK")
        return predicate

    ### OTHER TAIL RECURSIVE PRODUCTIONS ############################################################

    def scheme_list(self):
        """schemeList -> scheme schemeList | lambda
        FIRST(schemeList) = {ID}
        """
        # Production 1
        if self.get_curr_token().token_type == "ID":
            schemes = [self.scheme()]
            schemes += self.scheme_list()
            return schemes

        # Production 2
        else:
            return []
        

    def fact_list(self):
        """factList -> fact factList | lambda
        FIRST(factList) = {ID} 
        """
        # Production 1
        if self.get_curr_token().token_type == "ID":
            facts = [self.fact()]
            facts += self.fact_list()
            return facts
        
        # Production 2
        else:
            return []

    def rule_list(self):
        """ruleList -> rule ruleList | lambda 
        FIRST(ruleList) = {ID}
        """
        # Production 1
        if self.get_curr_token().token_type == "ID":
            rules = [self.rule()]
            rules += self.rule_list()
            return rules
        
        # Production 2
        else:
            return []

    def query_list(self):
        """queryList -> query queryList | lambda
        FIRST(queryList) = {ID}
        """
        # Production 1
        if self.get_curr_token().token_type == "ID":
            queries = [self.query()]
            queries += self.query_list()
            return queries
        
        # Production 2
        else:
            return []