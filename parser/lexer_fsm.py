from .fsa_classes.fsa import FSA

from .fsa_classes.colon_dash_fsa import ColonDashFSA
from .fsa_classes.colon_fsa import ColonFSA
from .fsa_classes.left_paren_fsa import LeftParenFSA
from .fsa_classes.right_paren_fsa import RightParenFSA
from .fsa_classes.comma_fsa import CommaFSA
from .fsa_classes.period_fsa import PeriodFSA
from .fsa_classes.q_mark_fsa import QMarkFSA
from .fsa_classes.multiply_fsa import MultiplyFSA
from .fsa_classes.add_fsa import AddFSA
from .fsa_classes.schemes_fsa import SchemesFSA
from .fsa_classes.facts_fsa import FactsFSA
from .fsa_classes.rules_fsa import RulesFSA
from .fsa_classes.queries_fsa import QueriesFSA
from .fsa_classes.id_fsa import IDFSA
from .fsa_classes.string_fsa import StringFSA
from .fsa_classes.comment_fsa import CommentFSA

from .my_token import Token

class LexerFSM:
    def __init__(self):
        self.tokens: list[Token] = []
        self.line_num: int = 1
        self.undefined: bool = False

        self.colon_dash_fsa: ColonDashFSA = ColonDashFSA()
        self.colon_fsa: ColonFSA = ColonFSA()
        self.right_paren_fsa: RightParenFSA = RightParenFSA()
        self.left_paren_fsa: LeftParenFSA = LeftParenFSA()
        self.comma_fsa: CommaFSA = CommaFSA()
        self.period_fsa: PeriodFSA = PeriodFSA()
        self.q_mark_fsa: QMarkFSA = QMarkFSA()
        self.multiply_fsa: MultiplyFSA = MultiplyFSA()
        self.add_fsa: AddFSA = AddFSA()
        self.schemes_fsa: SchemesFSA = SchemesFSA()
        self.facts_fsa: FactsFSA = FactsFSA()
        self.rules_fsa: RulesFSA = RulesFSA()
        self.queries_fsa: QueriesFSA = QueriesFSA()
        self.id_fsa: IDFSA = IDFSA()
        self.string_fsa: StringFSA = StringFSA()
        self.comment_fsa: CommentFSA = CommentFSA()
        
        # create list of FSAs
        self.fsas: list[FSA] = [
            self.string_fsa,
            self.schemes_fsa,
            self.queries_fsa,
            self.rules_fsa,
            self.facts_fsa,
            self.id_fsa,
            self.comment_fsa,
            self.colon_dash_fsa, 
            self.colon_fsa, 
            self.left_paren_fsa, 
            self.right_paren_fsa, 
            self.comma_fsa, 
            self.period_fsa, 
            self.q_mark_fsa,
            self.multiply_fsa,
            self.add_fsa
        ]    

    def run(self, input: str) -> str:
        self.reset()  # Clear the tokens list
        self.lex(input)  # call the lex method

        ans: str = ""  # output string of what is tokenized
        for token in self.tokens:
            ans += token.to_string() + "\n"

        # check if any undefined tokens
        if self.undefined:
            ans += "\nTotal Tokens = Error on line " + str(self.line_num)
        # else:
        #     # ans += "Total Tokens = " + str(len(self.tokens))
        
        return ans
    
    def lex(self, input_string: str) -> Token:
        if not input_string:
            self.undefined = False
            self.tokens.append(Token("EOF", "", self.line_num))
            return self.tokens
        
        # Iterating over the string
        while len(input_string) > 0:
            
            #get rid of leading whitespace
            while input_string and input_string[0].isspace():
                if input_string[0] == '\n':
                    # track line numbers
                    self.line_num += 1
                input_string = input_string[1:]

            self.undefined = True

            # Iterate through each FSA to find matches
            for fsa in self.fsas:
                
                # run the rest of the lexer if it doesn't encounter comments
                if fsa.run(input_string):
                    self.undefined = False
                    fsa.accepted = True
                    
                    self.tokens.append(Token(fsa.get_name(), input_string[:fsa.num_chars_read], self.line_num))
                    
                    input_string = input_string[fsa.num_chars_read:]
                    fsa.reset() 
                    break
                
                fsa.reset()

                if len(input_string) == 0:
                    self.undefined = False
                    self.tokens.append(Token("EOF", "", self.line_num))
                    return self.tokens
        
            if self.undefined:
                return self.tokens.append(Token("UNDEFINED",input_string[0], self.line_num))
            
            # remove comments from lexer tokens
            for token in self.tokens:
                if token.token_type == "COMMENT":
                    self.tokens.remove(token)
            
        return self.tokens

    def reset(self) -> None:
        # clear the tokens list
        self.tokens = []