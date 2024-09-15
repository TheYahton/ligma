from lexer import Lexer
from parser import Parser
from interpreter import metainterpret


# TODO: use sys.argv in main.py
# TODO: codegen
# TODO: add debug print in main
# TODO: improve functions and calls in parser and interpreter

if __name__ == "__main__":
    with open("examples/hello.lig", "r") as f:
        text = f.read()

    tokens = Lexer(text).all()
    ast = Parser(tokens).parse()
    metainterpret(ast)
