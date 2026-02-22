from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    """An enum representing the different types of tokens in NanoBASIC. Each
    token type has a regex pattern and a boolean indicating whether it has an
    associated value.
    """

    COMMENT = (r"rem.*", False)
    WHITESPACE = (r"[ \t\n\r]", False)
    PRINT = (r"print", False)
    IF_T = (r"if", False)
    THEN = (r"then", False)
    LET = (r"let", False)
    GOTO = (r"goto", False)
    GOSUB = (r"gosub", False)
    RETURN_T = (r"return", False)
    COMMA = (r",", False)
    EQUAL = (r"=", False)
    NOT_EQUAL = (r"<>|><", False)
    LESS_EQUAL = (r"<=", False)
    GREATER_EQUAL = (r">=", False)
    LESS = (r"<", False)
    GREATER = (r">", False)
    PLUS = (r"\+", False)
    MINUS = (r"-", False)
    MULTIPLY = (r"\*", False)
    DIVIDE = (r"/", False)
    OPEN_PAREN = (r"\(", False)
    CLOSE_PAREN = (r"\)", False)
    VARIABLE = (r"[A-Za-z_]+", True)
    NUMBER = (r"-?[0-9]+", True)
    STRING = (r'".*"', True)

    def __init__(self, pattern: str, has_associated_value: bool):
        """Initializes a TokenType with a regex pattern and a boolean indicating
        whether it has an associated value.

        Args:
            pattern (str): A regex pattern that matches the token type.
            has_associated_value (bool): A boolean indicating whether the token type has
                an associated value.
        """
        self.pattern = pattern
        self.has_associated_value = has_associated_value

    def __repr__(self) -> str:
        """Returns a string representation of the TokenType, which is just its name."""
        return self.name


@dataclass(frozen=True)
class Token:
    """A dataclass representing a token in NanoBASIC. Each token has a type,
    line number, starting column, ending column, and an optional associated value.
    """

    kind: TokenType
    line_num: int
    col_start: int
    col_end: int
    associated_value: str | int | None
