from tokens import TokenKind, Token, ONES, KEYWORDS


SPECIAL = Token(kind=TokenKind.Special)


class Lexer:
    def __init__(self, text: str):
        self.text: str = text

    def trim(self, i: int):
        self.text = self.text[i:]

    def until(self, what: str, start: int = 0) -> str:
        i = self.text.find(what, start) + len(what)
        content = self.text[:i]
        self.trim(i)
        return content

    def while_func(self, f) -> str:
        i = 0
        while i < len(self.text):
            if not f(self.text[: i + 1]):
                break
            i += 1
        content = self.text[:i]
        self.trim(i)
        return content

    def invalid(self):
        content = self.text[0]
        self.trim(1)
        return content

    def get_token(self):
        self.text = self.text.lstrip()

        match self.text:
            case "":
                token = Token(TokenKind.End)
            case x if x[0].isdecimal():
                content = int(self.while_func(str.isdecimal))
                token = Token(TokenKind.NumberLiteral, content)
            case x if x.startswith('"'):
                content = self.until('"', 1)
                token = Token(TokenKind.StringLiteral, content)
            case x if x.startswith("//"):
                content = self.until("\n")
                token = Token(TokenKind.Comment, content)
            case x if x.startswith("/*"):
                content = self.until("*/")
                token = Token(TokenKind.Comment, content)
            case x if x[0] in ONES:
                content = x[0]
                self.trim(1)
                token = Token(ONES[content], content)
            case x if x[0].isidentifier():
                content = self.while_func(str.isidentifier)
                token = Token(KEYWORDS.get(content, TokenKind.Id), content)
            case _:
                content = self.invalid()
                token = Token(TokenKind.Invalid, content)

        return token

    def all(self) -> list[Token]:
        output: list[Token] = []
        while True:
            token = self.get_token()
            output.append(token)
            if token.kind == TokenKind.End:
                break
        return output
