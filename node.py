from enum import Enum, auto
from dataclasses import dataclass


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
    func_name: str
    arg: Node | None


@dataclass(kw_only=True)
class BlockNode(Node):
    nodes: tuple[Node, ...]


@dataclass(kw_only=True)
class ProcNode(Node):
    name: str
    scope: BlockNode
