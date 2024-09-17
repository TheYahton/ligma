from __future__ import annotations
from enum import Enum, auto
from dataclasses import dataclass
from typing import Literal

from lexer import Token, TokenKind, SPECIAL


class BinaryKind(Enum):
    Add = auto()
    Sub = auto()
    Mul = auto()
    Div = auto()


@dataclass(kw_only=True)
class Node:
    pass


@dataclass(kw_only=True)
class NumberNode(Node):
    value: int


@dataclass(kw_only=True)
class VariableNode(Node):
    name: str


@dataclass(kw_only=True)
class BinaryNode(Node):
    kind: BinaryKind
    lhs: Node
    rhs: Node


@dataclass(kw_only=True)
class AssignNode(Node):
    var: VariableNode
    value: Node


@dataclass(kw_only=True)
class CallNode(Node):
    name: str
    arg: Node


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
                case TokenKind.Id:
                    arg = self._output.pop()
                    print = CallNode(name="print", arg=arg)
                    self._output.append(print)
                case TokenKind.Equal:
                    value = self._output.pop()
                    var = self._output.pop()
                    match var:
                        case VariableNode():
                            assign = AssignNode(var=var, value=value)
                            self._output.append(assign)
                        case _:
                            raise SyntaxError

    def _number(self, token):
        number = token.content
        node = NumberNode(value=number)
        self._output.append(node)

    def _id(self, token):
        if token.content == "print":
            self._stack.append(token)
            return
        node = VariableNode(name=token.content)
        self._output.append(node)

    def parse_statement(self) -> Node:
        while len(self._tokens) > 0:
            token = self._tokens.pop(0)
            match token.kind:
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
                case TokenKind.Semicolon:
                    break

        self._pop_stack(SPECIAL)

        return self._output.pop()

    def parse_all(self) -> list[Node]:
        output: list[Node] = []
        while len(self._tokens) > 0 and self._tokens[0].kind != TokenKind.End:
            output.append(self.parse_statement())
            self._stack.clear()
            self._output.clear()

        return output
