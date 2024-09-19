import sys
from os import get_terminal_size

from lexer import Lexer
from parser import Parser
from interpreter import metainterpret


# TODO: кодогенерация
# TODO: переосмыслить вызов функции print
# TODO: если написано что-то кроме интерпретатора, то добавить флаги для этого
# TODO: добавить систему типов
# TODO: добавить обработку скобок в парсере
# TODO: переписать лексер - использовать конечные автоматы (FSM)
# TODO: переписать парсер - использовать конечные автоматы (FSM)

WIDTH, _ = get_terminal_size()


def dprint(debug: bool, *args, **kwargs):
    if debug:
        print(*args, **kwargs)


def print_tokens(debug: bool, tokens):
    dprint(debug)
    dprint(debug)
    dprint(debug, "TOKENS")
    dprint(debug, "-" * WIDTH)
    dprint(debug, *tokens, sep="\n")
    dprint(debug, "-" * WIDTH)


def print_ast(debug: bool, ast):
    dprint(debug)
    dprint(debug)
    dprint(debug, "AST")
    dprint(debug, "-" * WIDTH)
    dprint(debug, *ast, sep="\n\n")
    dprint(debug, "-" * WIDTH)


def print_interpret(debug: bool):
    dprint(debug)
    dprint(debug)
    dprint(debug, "INTERPRET")


def read_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def main():
    args = sys.argv
    program_name, *args = args

    if len(args) == 0:
        print(f"Usage: {program_name} filename")
        return

    path, *args = args

    debug = False
    if "-debug" in args:
        args = args.remove("-debug")
        debug = True

    text = read_file(path)

    tokens = Lexer(text).all()
    print_tokens(debug, tokens)

    ast = Parser(tokens).parse_all()
    print_ast(debug, ast)

    print_interpret(debug)
    metainterpret(ast)


if __name__ == "__main__":
    main()
