from lexer import Token, TokenKind, SPECIAL
from node import *


def arith2binary(kind: TokenKind) -> BinaryKind:
    match kind:
        case TokenKind.Plus:
            return BinaryKind.Add
        case TokenKind.Minus:
            return BinaryKind.Sub
        case TokenKind.Asterisk:
            return BinaryKind.Mul
        case TokenKind.Slash:
            return BinaryKind.Div
    raise Exception


class Parser:
    def __init__(self, tokens: list[Token]):
        self._tokens = tokens
        self._stack: list[Token] = []
        self._output: list[Node] = []

    def _pop_stack(self, op1: Token):
        while len(self._stack) > 0 and (self._stack[-1].prec() >= op1.prec()):
            op2 = self._stack.pop()
            match op2.kind:
                case (
                    TokenKind.Plus
                    | TokenKind.Minus
                    | TokenKind.Asterisk
                    | TokenKind.Slash as x
                ):
                    rhs = self._output.pop()
                    lhs = self._output.pop()
                    op = BinaryNode(lhs=lhs, rhs=rhs, kind=arith2binary(x))
                    self._output.append(op)
                case TokenKind.Equal:
                    value = self._output.pop()
                    var = self._output.pop()
                    match var:
                        case VariableNode():
                            assign = AssignNode(var=var, value=value)
                            self._output.append(assign)
                        case _:
                            raise SyntaxError
                case _:
                    raise SyntaxError(f"unexpected op {op2}")

    def _number(self, token):
        number = token.content
        node = NumberNode(value=number)
        self._output.append(node)

    def _id(self, token):
        node = VariableNode(name=token.content)
        self._output.append(node)

    def _scope(self, balance: int = 1):
        i = 0
        while i < len(self._tokens):
            if self._tokens[i].kind == TokenKind.LBrace:
                balance += 1
            elif self._tokens[i].kind == TokenKind.RBrace:
                balance -= 1

            if balance == 0:
                break
            i += 1
        parser = Parser(self._tokens[0:i])
        node = BlockNode(nodes=tuple(parser.parse_all()))
        self._output.append(node)
        self._tokens[0 : i + 1] = []

    def _proc(self):
        name = self._tokens.pop(0)
        self._tokens.pop(0)
        self._scope()
        node = ProcNode(name=name.content, body=self._output.pop())
        self._output.append(node)

    def parse_statement(self) -> Node | None:
        while len(self._tokens) > 0:
            token = self._tokens.pop(0)
            match token.kind:
                case TokenKind.Comment:
                    pass
                case TokenKind.LBrace:
                    self._scope()
                case TokenKind.NumberLiteral:
                    self._number(token)
                case TokenKind.Id:
                    self._id(token)
                case (
                    TokenKind.Plus
                    | TokenKind.Minus
                    | TokenKind.Asterisk
                    | TokenKind.Slash
                    | TokenKind.Equal
                ):
                    self._pop_stack(token)
                    self._stack.append(token)
                case TokenKind.Proc:
                    self._proc()
                case TokenKind.Call:
                    name = self._tokens.pop(0)
                    semi = self._tokens.index(Token(TokenKind.Semicolon, ";"))
                    parser = Parser(self._tokens[0:semi])
                    arg = parser.parse_statement()
                    node = CallNode(func_name=name.content, arg=arg)
                    self._output.append(node)
                    self._tokens[0:semi] = []

                case TokenKind.Semicolon:
                    break
                case TokenKind.LParen | TokenKind.RParen:
                    # TODO
                    pass
                case TokenKind.End:
                    break
                case _:
                    raise SyntaxError(f"unexpected token: {token}")

        self._pop_stack(SPECIAL)

        if len(self._output) > 0:
            return self._output.pop()
        return None

    def parse_all(self) -> list[Node]:
        output: list[Node] = []
        while len(self._tokens) > 0 and self._tokens[0].kind != TokenKind.End:
            statement = self.parse_statement()
            if statement is None:
                break
            output.append(statement)
            self._stack.clear()
            self._output.clear()

        return output
