from __future__ import annotations
from dataclasses import dataclass, field

from node import (
    Node,
    BinaryKind,
    NumberNode,
    BinaryNode,
    AssignNode,
    VariableNode,
    CallNode,
    BlockNode,
    ProcNode,
)


@dataclass
class Scope:
    variables: dict[str, int | None] = field(default_factory=lambda: {})
    procedures: dict[str, ProcNode] = field(default_factory=lambda: {})
    parent: Scope | None = None

    def get_var(self, name: str) -> int | None:
        if name in self.variables:
            return self.variables[name]
        if self.parent is not None:
            return self.parent.get_var(name)
        else:
            return None

    def get_proc(self, name: str) -> ProcNode | None:
        if name in self.procedures:
            return self.procedures[name]
        if self.parent is not None:
            return self.parent.get_proc(name)
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
        case ProcNode() as x:
            proc_name = x.name
            scope.procedures.update({proc_name: x})
        case CallNode() as x:
            func = x.func_name
            value = None
            if x.arg is not None:
                value = interpret(x.arg, scope)

            if (proc := scope.get_proc(func)) is not None:
                interpret(proc.body, scope)
            if func == "print":
                print(value)

        case BlockNode() as x:
            local_scope = Scope(parent=scope)
            for node in x.nodes:
                result = interpret(node, local_scope)
            return result
        case _:
            raise SyntaxError(f"unexpected node {ast}")

    return None


def metainterpret(ast: list[Node]):
    global_scope = Scope()
    for a in ast:
        interpret(a, global_scope)
