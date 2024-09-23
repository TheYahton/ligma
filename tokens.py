from enum import Enum, auto
from dataclasses import dataclass


class TokenKind(Enum):
    End = auto()
    Invalid = auto()
    Comment = auto()
    Id = auto()

    LParen = auto()  # (
    RParen = auto()  # )
    LBrace = auto()  # {
    RBrace = auto()  # }
    LBracket = auto()  # [
    RBracket = auto()  # ]

    Colon = auto()  # :
    Semicolon = auto()  # ;
    Dot = auto()  # .
    Comma = auto()  # ,

    Plus = auto()  # +
    Minus = auto()  # -
    Asterisk = auto()  # *
    Slash = auto()  # /

    Equal = auto()  # =

    StringLiteral = auto()
    NumberLiteral = auto()

    # Keywords
    Proc = auto()
    Return = auto()
    Call = auto()

    Special = auto()


KEYWORDS = {
    "proc": TokenKind.Proc,
    "return": TokenKind.Return,
    "call": TokenKind.Call,
}

ONES = {
    "(": TokenKind.LParen,
    ")": TokenKind.RParen,
    "{": TokenKind.LBrace,
    "}": TokenKind.RBrace,
    "[": TokenKind.LBracket,
    "]": TokenKind.RBracket,
    ":": TokenKind.Colon,
    ";": TokenKind.Semicolon,
    ".": TokenKind.Dot,
    ",": TokenKind.Comma,
    "+": TokenKind.Plus,
    "-": TokenKind.Minus,
    "*": TokenKind.Asterisk,
    "/": TokenKind.Slash,
    "=": TokenKind.Equal,
}


@dataclass
class Token:
    kind: TokenKind
    content: str = ""

    def prec(self) -> int:
        match self.kind:
            case TokenKind.Special:
                return -1000
            case TokenKind.Equal:
                return 0
            case TokenKind.Plus | TokenKind.Minus:
                return 1
            case TokenKind.Asterisk | TokenKind.Slash:
                return 2
        return 1000
