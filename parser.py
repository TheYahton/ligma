from __future__ import annotations
from enum import Enum, auto
from dataclasses import dataclass
from typing import Literal

from lexer import Token, TokenKind


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


class Parser:
    def __init__(self, tokens: list[Token]):
        self._tokens = tokens
        self._stack: list[Token] = []
        self._output: list[Node] = []

    def _pop_stack(self):
        while len(self._stack) > 0:
            smth = self._stack.pop()
            match smth.kind:
                case TokenKind.Plus:
                    rhs = self._output.pop()
                    lhs = self._output.pop()
                    op = BinaryNode(lhs=lhs, rhs=rhs, kind=BinaryKind.Add)
                    self._output.append(op)
                case TokenKind.Minus:
                    rhs = self._output.pop()
                    lhs = self._output.pop()
                    op = BinaryNode(lhs=lhs, rhs=rhs, kind=BinaryKind.Sub)
                    self._output.append(op)
                case TokenKind.Asterisk:
                    rhs = self._output.pop()
                    lhs = self._output.pop()
                    op = BinaryNode(lhs=lhs, rhs=rhs, kind=BinaryKind.Mul)
                    self._output.append(op)
                case TokenKind.Slash:
                    rhs = self._output.pop()
                    lhs = self._output.pop()
                    op = BinaryNode(lhs=lhs, rhs=rhs, kind=BinaryKind.Div)
                    self._output.append(op)
                case TokenKind.Id:
                    arg = self._output.pop()
                    print = CallNode(name="print", arg=arg)
                    self._output.append(print)

    def _number(self, token):
        number = token.content
        node = NumberNode(value=int(number))
        self._output.append(node)

    def _id(self, token):
        if token.content == "print":
            self._stack.append(token)
            return
        node = VariableNode(name=token.content)
        self._output.append(node)

    def _let(self, token):
        let = token
        name = self._tokens.pop(0)
        equal = self._tokens.pop(0)
        semicolon_index = self._tokens.index(Token(TokenKind.Semicolon, ";"))
        raw_statement = self._tokens[:semicolon_index]
        self._tokens = self._tokens[semicolon_index:]
        semicolon = self._tokens.pop(0)

        parser = Parser(raw_statement)
        statement = parser.parse().pop()
        node = AssignNode(
            var=VariableNode(name=name.content),
            value=statement,
        )
        self._output.append(node)

    def parse(self) -> list[Node]:
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
                ):
                    self._pop_stack()
                    self._stack.append(token)
                case TokenKind.Let:
                    self._let(token)

        self._pop_stack()

        return self._output
