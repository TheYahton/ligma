from dataclasses import dataclass

from parser import (
    Node,
    NodeKind,
    NumberNode,
    BinaryNode,
    AssignNode,
    VariableNode,
    CallNode,
)


@dataclass
class Scope:
    variables: dict[str, int | None]


def interpret(ast: Node | str | int, scope: Scope):
    if not isinstance(ast, Node):
        raise TypeError

    match ast:
        case NumberNode() as x:
            return x.children[0]
        case BinaryNode() as x:
            lhs = interpret(x.children[0], scope)
            rhs = interpret(x.children[1], scope)
            match x.type:
                case NodeKind.Add:
                    return lhs + rhs
                case NodeKind.Sub:
                    return lhs - rhs
        case AssignNode() as x:
            name = interpret(x.children[0], scope)
            value = interpret(x.children[1], scope)
            if name in scope.variables:
                scope.variables.update({name: value})
            return value
        case VariableNode(type=NodeKind.InitVar) as x:
            scope.variables.update({x.children[0]: None})
            return x.children[0]
        case VariableNode(type=NodeKind.GetVar) as x:
            if x.children[0] not in scope.variables:
                raise SyntaxError
            return scope.variables[x.children[0]]
        case CallNode() as x:
            value = interpret(x.children[1], scope)
            func = x.children[0]
            match func:
                case "print":
                    print(value)

    return 0


def metainterpret(ast: list[Node]):
    scope = Scope({})
    for a in ast:
        interpret(a, scope)
