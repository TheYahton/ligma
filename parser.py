from __future__ import annotations
from enum import Enum, auto
from dataclasses import dataclass
from typing import Literal

from lexer import Token, TokenKind


class NodeKind(Enum):
    Number = auto()
    Id = auto()
    Print = auto()

    InitVar = auto()
    GetVar = auto()
    Assign = auto()

    Call = auto()

    Add = auto()
    Sub = auto()

    Count = auto()


@dataclass(kw_only=True)
class Node:
    children: tuple[Node | int | str, ...]
    type: NodeKind


@dataclass(kw_only=True)
class NumberNode(Node):
    children: tuple[int]
    type: Literal[NodeKind.Number] = NodeKind.Number


@dataclass(kw_only=True)
class VariableNode(Node):
    children: tuple[str]
    type: Literal[NodeKind.InitVar] | Literal[NodeKind.GetVar]


@dataclass(kw_only=True)
class BinaryNode(Node):
    children: tuple[Node, Node]


@dataclass(kw_only=True)
class AssignNode(Node):
    children: tuple[VariableNode, NumberNode]
    type: Literal[NodeKind.Assign] = NodeKind.Assign


@dataclass(kw_only=True)
class CallNode(Node):
    children: tuple[str, Node]
    type: Literal[NodeKind.Call] = NodeKind.Call


class Parser:
    def __init__(self, tokens: list[Token]):
        self._tokens = tokens
        self._stack: list[Token] = []
        self._output: list[Node] = []

    def _pop_stack(self):
        while len(self._stack) > 0:
            op = self._stack.pop()
            match op.kind:
                case TokenKind.Plus:
                    rhs = self._output.pop()
                    lhs = self._output.pop()
                    add = BinaryNode(children=(lhs, rhs), type=NodeKind.Add)
                    self._output.append(add)
                case TokenKind.Id:
                    arg = self._output.pop()
                    print = CallNode(children=("print", arg))
                    self._output.append(print)

    def _number(self, token):
        number = token.content
        node = NumberNode(children=(int(number),))
        self._output.append(node)

    def _id(self, token):
        if token.content == "print":
            self._stack.append(token)
            return
        node = VariableNode(children=(token.content,), type=NodeKind.GetVar)
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
            children=(
                VariableNode(children=(name.content,), type=NodeKind.InitVar),
                statement,
            ),
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
                case TokenKind.Plus:
                    self._pop_stack()
                    self._stack.append(token)
                case TokenKind.Let:
                    self._let(token)

        self._pop_stack()

        return self._output
