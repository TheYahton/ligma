from lexer import Lexer


# TODO: use sys.argv in main.py
# TODO: parser
# TODO: interpreter
# TODO: codegen

if __name__ == "__main__":
    with open("examples/hello.lig", "r") as f:
        text = f.read()

    tokens = Lexer(text).all()
    print(*tokens, sep="\n")
