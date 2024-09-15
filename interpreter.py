from dataclasses import dataclass

from parser import (
    Node,
    BinaryKind,
    NumberNode,
    BinaryNode,
    AssignNode,
    VariableNode,
    CallNode,
)


@dataclass
class Scope:
    variables: dict[str, int | None]


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
            return scope.variables[x.name]
        case CallNode() as x:
            value = interpret(x.arg, scope)
            func = x.name
            match func:
                case "print":
                    print(value)

    return 0


def metainterpret(ast: list[Node]):
    scope = Scope({})
    for a in ast:
        interpret(a, scope)


# TODO: rethink about scopes
# TODO: rethink about functions
