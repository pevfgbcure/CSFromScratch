from dataclasses import dataclass

from NanoBASIC.tokenizer import TokenType


@dataclass(frozen=True)
class Node:
    """Base class for all nodes in the AST.

    - *line_num* is the line number in the source code where this node appears.
    - *col_start* is the starting column number of this node in the source code.
    - *col_end* is the ending column number of this node in the source code.
    """

    line_num: int
    col_start: int
    col_end: int


@dataclass(frozen=True)
class Statement(Node):
    """Base class for all statements in the AST.

    - *line_id* is an identifier that the programmer puts in before the statement.
        For example, in the line "10 PRINT 'HELLO'", the line_id would be 10.
        This is used for GOTO and GOSUB statements.
    """

    line_id: int


@dataclass(frozen=True)
class NumericExpression(Node):
    """A numeric expression is something that can be computed into a number.

    - This is a superclass for literals, variables and simple arithmetic operations.
    """

    pass


@dataclass(frozen=True)
class BinaryOperation(NumericExpression):
    """Represents a numeric expression with two operands, like 2 + 2 or 8 / 4."""

    operator: TokenType
    left_expr: NumericExpression
    right_expr: NumericExpression

    def __repr__(self) -> str:
        return f"{self.left_expr} {self.operator} {self.right_expr}"


@dataclass(frozen=True)
class UnaryOperation(NumericExpression):
    """Represents a numeric expressions with one operand, like -4."""

    operator: TokenType
    expr: NumericExpression

    def __repr__(self) -> str:
        return f"{self.operator}{self.expr}"


@dataclass(frozen=True)
class NumberLiteral(NumericExpression):
    """Represents an integer written out in the source code, like 6 or 7."""

    number: int


@dataclass(frozen=True)
class VarRetrieve(NumericExpression):
    """Represents a variable's *name* that will have its value retrieved."""

    name: str


@dataclass(frozen=True)
class BooleanExpression(Node):
    """Represents a boolean expression that can be computed to true or false.

    - It takes two numeric expressions, *left_expr* and *right_expr*, and compares
    them using a boolean *operator*.
    """

    operator: TokenType
    left_expr: NumericExpression
    right_expr: NumericExpression

    def __repr__(self):
        return f"{self.left_expr} {self.operator} {self.right_expr}"


@dataclass(frozen=True)
class LetStatement(Statement):
    """Represents a LET statement, setting *name* to *expr*."""

    name: str
    expr: NumericExpression


@dataclass(frozen=True)
class GoToStatement(Statement):
    """Represents a GOTO statement, transferring control to *line_expr*."""

    line_expr: NumericExpression


@dataclass(frozen=True)
class GoSubStatement(Statement):
    """Represents a GOSUB statement, transferring control to *line_expr*.

    NOTE:
        Return *line_id* is not saved here, it will be maintained by a stack.
    """

    line_expr: NumericExpression


@dataclass(frozen=True)
class ReturnStatement(Statement):
    """Represents a RETURN statement, transferring control to the line after
    the last GOSUB statement.
    """

    pass


@dataclass(frozen=True)
class PrintStatement(Statement):
    """Represents a PRINT statement with all that it's meant to print
    (comma separated).
    """

    printables: list[str | NumericExpression]


@dataclass(frozen=True)
class IfStatement(Statement):
    """Represents an IF statement.

    - The *then_statement* is what statement will be executed if the
    *boolean_expr* is true.
    """

    boolean_expr: BooleanExpression
    then_statement: Statement
