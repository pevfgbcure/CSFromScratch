import re
from dataclasses import dataclass
from enum import Enum
from typing import TextIO


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
    STRING = (r'"(?:[^"\\]|\\.)*"', True)

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


def tokenize(text_file: TextIO) -> list[Token]:
    """Tokenizes a text file containing NanoBASIC code.

    - Each token is represented as a Token dataclass, which contains the token type, line
      number, starting column, ending column, and an optional associated value.

    Args:
        text_file (TextIO): A text file containing NanoBASIC code.

    Returns:
        list[Token]: A list of tokens found in the text file.
    """
    tokens: list[Token] = []
    for line_num, line in enumerate(text_file.readlines(), start=1):
        col_start: int = 1

        while len(line) > 0:
            found: re.Match | None = None
            for possibility in TokenType:
                # Try each pattern in the enum from the beginning, case-insensitive.
                # If a match is found, store it in found.
                found = re.match(possibility.pattern, line, re.IGNORECASE)
                if found:
                    col_end: int = col_start + found.end() - 1
                    # Store tokens other than comments and whitespace.
                    if (
                        possibility is not TokenType.WHITESPACE
                        and possibility is not TokenType.COMMENT
                    ):
                        associated_value: str | int | None = None
                        if possibility.has_associated_value:
                            if possibility is TokenType.NUMBER:
                                associated_value = int(found.group(0))
                            elif possibility is TokenType.VARIABLE:
                                associated_value = found.group()
                            elif possibility is TokenType.STRING:
                                # Remove quotation marks and unescape escapes.
                                raw_text: str = found.group(0)[1:-1]
                                associated_value = raw_text.replace('\\"', '"')
                        tokens.append(
                            Token(
                                possibility,
                                line_num,
                                col_start,
                                col_end,
                                associated_value,
                            )
                        )

                    # Continue search for tokens in the same line, but after the current token.
                    line = line[found.end() :]
                    col_start = col_end + 1
                    break  # Go around again for the next token.

            # If we went through all the tokens and none of them were a match,
            # then this must be an invalid token.
            if not found:
                print(f"Syntax error on line {line_num} column {col_start}")
                break

    return tokens
