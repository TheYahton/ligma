from tokens import TokenKind, Token, ONES, KEYWORDS


SPECIAL = Token(kind=TokenKind.Special)


class Lexer:
    def __init__(self, text: str):
        self._text: str = text

    def _trim(self, i: int):
        self._text = self._text[i:]

    def _until(self, what: str, start: int = 0) -> str:
        i = self._text.find(what, start) + len(what)
        content = self._text[:i]
        self._trim(i)
        return content

    def _while_func(self, f) -> str:
        i = 0
        while i < len(self._text):
            if not f(self._text[: i + 1]):
                break
            i += 1
        content = self._text[:i]
        self._trim(i)
        return content

    def _invalid(self):
        content = self._text[0]
        self._trim(1)
        return content

    def get_token(self):
        self._text = self._text.lstrip()

        match self._text:
            case "":
                token = Token(TokenKind.End)
            case x if x[0].isdecimal():
                content = int(self._while_func(str.isdecimal))
                token = Token(TokenKind.NumberLiteral, content)
            case x if x.startswith('"'):
                content = self._until('"', 1)
                token = Token(TokenKind.StringLiteral, content)
            case x if x.startswith("//"):
                content = self._until("\n")
                token = Token(TokenKind.Comment, content)
            case x if x.startswith("/*"):
                content = self._until("*/")
                token = Token(TokenKind.Comment, content)
            case x if x[0] in ONES:
                content = x[0]
                self._trim(1)
                token = Token(ONES[content], content)
            case x if x[0].isidentifier():
                content = self._while_func(str.isidentifier)
                token = Token(KEYWORDS.get(content, TokenKind.Id), content)
            case _:
                content = self._invalid()
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
