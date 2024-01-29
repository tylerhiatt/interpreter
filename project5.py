from parser.lexer_fsm import LexerFSM
from parser.my_parser import Parser
from interpreter import Interpreter

#Return your program output here for grading (can treat this function as your "main")
def project5(input: str) -> str:
    lexer = LexerFSM()
    tokens = lexer.lex(input)

    parser: Parser = Parser()
    datalog_program = parser.run(tokens)

    interpreter: Interpreter = Interpreter()
    # print(interpreter.run(datalog_program))
    return interpreter.run(datalog_program)

def read_file_contents(filepath):
    with open(filepath, "r") as f:
        return f.read() 

#Use this to run and debug code within VS
if __name__ == "__main__":
    input_contents = read_file_contents("project5-passoff/80/input2.txt")
    print(project5(input_contents))
