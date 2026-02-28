from NanoBASIC.nodes import Node
from NanoBASIC.tokenizer import Token


class NanoBASICError(Exception):
    """Base class for all NanoBASIC errors."""

    def __init__(self, message: str, line_num: int, column: int):
        """Initializes the error with a message, line number, and column number."""
        super().__init__(message)
        self.message = message
        self.line_num = line_num
        self.column = column

    def __str__(self):
        """Returns a string representation of the error, including the message and location."""
        return (
            f"{self.message} Ocurred at line {self.line_num} and column {self.column}"
        )


class ParserError(NanoBASICError):
    """Raised when a syntax error is encountered during parsing."""

    def __init__(self, message: str, token: Token):
        """Initializes the error with a message and the token that caused the error."""
        super().__init__(message, token.line_num, token.col_start)


class InterpreterError(NanoBASICError):
    """Raised when a runtime error is encountered during interpretation."""

    def __init__(self, message: str, node: Node):
        """Initializes the error with a message and the node that caused the error."""
        super().__init__(message, node.line_num, node.col_start)
