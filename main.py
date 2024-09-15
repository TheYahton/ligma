import sys

from lexer import Lexer
from parser import Parser
from interpreter import metainterpret


# TODO: codegen
# TODO: add debug print in main
# TODO: improve functions and calls in parser and interpreter
# TODO: if compiler exist, add flags to compile or execute


def main():
    program_name = sys.argv[0]
    if len(sys.argv) != 2:
        print(f"Usage: {program_name} filename")
        return

    path = sys.argv[1]

    with open(path, "r") as f:
        text = f.read()

    tokens = Lexer(text).all()
    ast = Parser(tokens).parse()
    metainterpret(ast)


if __name__ == "__main__":
    main()
