import os
from my_token import Token
from my_parser import Parser
from lexer_fsm import LexerFSM

#Return your program output here for grading (can treat this function as your "main")
def project2(input: str) -> str:
    # grab stuff from project one over
    lexer = LexerFSM()
    tokens = lexer.lex(input)

    # this is our example list of tokens, for the actual project you will use the lexer to generate this
    # test out scheme
    # tokens = [
    #     Token("ID", "snap", 1),
    #     Token("LEFT_PAREN", "(", 1),
    #     Token("ID", "StudentId", 1),
    #     Token("COMMA", ",", 1),
    #     Token("ID", "Name", 1),
    #     Token("COMMA", ",", 1),
    #     Token("ID", "Address", 1),
    #     Token("COMMA", ",", 1),
    #     Token("ID", "PhoneNumber", 1),
    #     Token("RIGHT_PAREN", ")", 1)
    # ]
    # print(tokens)
    # # test out fact
    # tokens = [
    #     Token("ID", "snap", 1),
    #     Token("LEFT_PAREN", "(", 1),
    #     Token("STRING", "string1", 1),
    #     Token("COMMA", ",", 1),
    #     Token("STRING", "string2", 1),
    #     Token("COMMA", ",", 1),
    #     Token("STRING", "string3", 1),
    #     Token("RIGHT_PAREN", ")", 1),
    #     Token("PERIOD", ".", 1)
    # ]
    # test out rule
    # tokens = [
    #     Token("ID", "Rule1", 1),
    #     Token("LEFT_PAREN", "(", 1),
    #     Token("ID", "Param1", 1),
    #     Token("COMMA", ",", 1),
    #     Token("ID", "Param2", 1),
    #     Token("RIGHT_PAREN", ")", 1),
    #     Token("COLON_DASH", ":-", 1),
    #     Token("ID", "HeadPred", 1),
    #     Token("LEFT_PAREN", "(", 1),
    #     Token("ID", "HeadParam", 1),
    #     Token("RIGHT_PAREN", ")", 1),
    #     Token("COMMA", ",", 1),
    #     Token("ID", "BodyPred1", 1),
    #     Token("LEFT_PAREN", "(", 1),
    #     Token("ID", "BodyParam1", 1),
    #     Token("RIGHT_PAREN", ")", 1),
    #     Token("COMMA", ",", 1),
    #     Token("ID", "BodyPred2", 1),
    #     Token("LEFT_PAREN", "(", 1),
    #     Token("ID", "BodyParam2", 1),
    #     Token("RIGHT_PAREN", ")", 1),
    #     Token("PERIOD", ".", 1),
    #     Token("ID", "Rule2", 2),
    #     Token("LEFT_PAREN", "(", 2),
    #     Token("ID", "Param3", 2),
    #     Token("COMMA", ",", 2),
    #     Token("ID", "Param4", 2),
    #     Token("RIGHT_PAREN", ")", 2),
    #     Token("COLON_DASH", ":-", 2),
    #     Token("ID", "HeadPred2", 2),
    #     Token("LEFT_PAREN", "(", 2),
    #     Token("ID", "HeadParam2", 2),
    #     Token("RIGHT_PAREN", ")", 2),
    #     Token("PERIOD", ".", 2),
    # ]

    # # test out query 
    # tokens = [
    #     Token("ID", "Query1", 1),
    #     Token("LEFT_PAREN", "(", 1),
    #     Token("ID", "Param1", 1),
    #     Token("COMMA", ",", 1),
    #     Token("ID", "Param2", 1),
    #     Token("RIGHT_PAREN", ")", 1),
    #     Token("Q_MARK", "?", 1),
    #     Token("ID", "Query2", 2),
    #     Token("LEFT_PAREN", "(", 2),
    #     Token("ID", "Param3", 2),
    #     Token("RIGHT_PAREN", ")", 2),
    #     Token("Q_MARK", "?", 2),
    #     Token("EOF", "", 2)
    # ]

    # test out datalogProgram
    # tokens = [
    #     Token("SCHEMES", "SCHEMES", 1),
    #     Token("COLON", ":", 1),
    #     Token("ID", "scheme1", 1),
    #     Token("LEFT_PAREN", "(", 1),
    #     Token("ID", "param1", 1),
    #     Token("COMMA", ",", 1),
    #     Token("ID", "param2", 1),
    #     Token("RIGHT_PAREN", ")", 1),
    #     Token("ID", "scheme2", 1),
    #     Token("LEFT_PAREN", "(", 1),
    #     Token("ID", "param3", 1),
    #     Token("COMMA", ",", 1),
    #     Token("ID", "param4", 1),
    #     Token("RIGHT_PAREN", ")", 1),
    #     Token("FACTS", "FACTS", 1),
    #     Token("COLON", ":", 1),
    #     Token("ID", "fact1", 1),
    #     Token("LEFT_PAREN", "(", 1),
    #     Token("STRING", "fact_string", 1),
    #     Token("RIGHT_PAREN", ")", 1),
    #     Token("PERIOD", ".", 1),
    #     Token("RULES", "RULES", 1),
    #     Token("COLON", ":", 1),
    #     Token("ID", "rule1", 1),
    #     Token("LEFT_PAREN", "(", 1),
    #     Token("ID", "param1", 1),
    #     Token("COMMA", ",", 1),
    #     Token("ID", "param2", 1),
    #     Token("RIGHT_PAREN", ")", 1),
    #     Token("COLON_DASH", ":-", 1),
    #     Token("ID", "predicate1", 1),
    #     Token("LEFT_PAREN", "(", 1),
    #     Token("ID", "param1", 1),
    #     Token("COMMA", ",", 1),
    #     Token("ID", "param2", 1),
    #     Token("RIGHT_PAREN", ")", 1),
    #     Token("PERIOD", ".", 1),
    #     Token("QUERIES", "QUERIES", 1),
    #     Token("COLON", ":", 1),
    #     Token("ID", "query1", 1),
    #     Token("LEFT_PAREN", "(", 1),
    #     Token("ID", "param1", 1),
    #     Token("COMMA", ",", 1),
    #     Token("ID", "param2", 1),
    #     Token("RIGHT_PAREN", ")", 1),
    #     Token("Q_MARK", "?", 1),
    #     Token("EOF", "", 1)
    # ]

    parser = Parser()

    #print(parser.run(tokens))
    return parser.run(tokens)

def read_file_contents(filepath):
    with open(filepath, "r") as f:
        return f.read() 

#Use this to run and debug code within VS
if __name__ == "__main__":
    os.chdir('.')
    input_contents = read_file_contents("project2-passoff/80/input0.txt")
    project2(input_contents)
    # input_contents = "some string"
    # print(project2(input_contents))
