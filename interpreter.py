from __future__ import annotations
from dataclasses import dataclass

from parser import (
    Node,
    BinaryKind,
    NumberNode,
    BinaryNode,
    AssignNode,
    VariableNode,
    CallNode,
    ScopeNode,
)


@dataclass
class Scope:
    variables: dict[str, int | None]
    parent: Scope | None = None

    def get_var(self, name: str):
        if name in self.variables:
            return self.variables[name]
        if self.parent is not None:
            return self.parent.get_var(name)
        else:
            return None


def interpret(ast: Node, scope: Scope):
    match ast:
        case NumberNode() as x:
            return x.value
        case BinaryNode() as x:
            lhs = interpret(x.lhs, scope)
            rhs = interpret(x.rhs, scope)
            match x.kind:
                case BinaryKind.Add:
                    return lhs + rhs
                case BinaryKind.Sub:
                    return lhs - rhs
                case BinaryKind.Mul:
                    return lhs * rhs
                case BinaryKind.Div:
                    return lhs / rhs
        case AssignNode() as x:
            name = x.var.name
            value = interpret(x.value, scope)
            scope.variables.update({name: value})
            return value
        case VariableNode() as x:
            return scope.get_var(x.name)
        case CallNode() as x:
            value = interpret(x.arg, scope)
            func = x.name
            match func:
                case "print":
                    print(value)
        case ScopeNode() as x:
            local_scope = Scope({}, scope)
            for node in x.nodes:
                result = interpret(node, local_scope)
            return result

    return 0


def metainterpret(ast: list[Node]):
    global_scope = Scope({})
    for a in ast:
        interpret(a, global_scope)


# TODO: rethink about functions
