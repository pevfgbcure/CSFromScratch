from collections import deque

import NanoBASIC.nodes as nodes
from NanoBASIC.errors import InterpreterError
from NanoBASIC.tokenizer import TokenType


class Interpreter:
    """Interprets a list of statements, maintaining variable state and control flow."""

    def __init__(self, statements: list[nodes.Statement]):
        """Initializes the interpreter with a list of statements and the runtime environment.

        Args:
            statements: A list of statements to interpret, sorted by line_id.
        """
        self.statements = statements
        # Keeps track of variable names and their integer values.
        self.variable_table: dict[str, int] = {}
        self.statement_index: int = 0
        # A stack to keep track of subroutine calls, storing the index of the statement to return to.
        self.subroutine_stack: deque[int] = deque()

    @property
    def current(self) -> nodes.Statement:
        """Returns the current statement being executed."""
        return self.statements[self.statement_index]

    def find_line_index(self, line_id: int) -> int | None:
        """Finds the index of the statement with the given line_id using binary search.
        Assumes that the statements list is sorted by line_id.

        Args:
            line_id: The line number to find.

        Returns:
            The index of the statement with the given line_id, or None if not found.
        """
        low: int = 0
        high: int = len(self.statements) - 1
        while low <= high:
            mid: int = (low + high) // 2
            if self.statements[mid].line_id < line_id:
                low = mid + 1
            elif self.statements[mid].line_id > line_id:
                high = mid - 1
            else:
                return mid

        return None

    def run(self):
        """Runs the interpreter, executing statements until the end of the list is reached."""
        while self.statement_index < len(self.statements):
            self.interpret(self.current)

    def interpret(self, statement: nodes.Statement):
        """Interprets a single statement, modifying the interpreter's state as needed.

        Args:
            statement: The statement to interpret.

        Raises:
            InterpreterError: If an error occurs during interpretation, such as an undefined
            variable or invalid control flow.
        """
        match statement:
            case nodes.LetStatement(name=name, expr=expr):
                value = self.evaluate_numeric(expr)
                self.variable_table[name] = value
                self.statement_index += 1

            case nodes.GoToStatement(line_expr=line_expr):
                go_to_line_id = self.evaluate_numeric(line_expr)
                if (line_index := self.find_line_index(go_to_line_id)) is not None:
                    self.statement_index = line_index
                else:
                    raise InterpreterError("No GOTO line id.", self.current)

            case nodes.GoSubStatement(line_expr=line_expr):
                go_sub_line_id = self.evaluate_numeric(line_expr)
                if (line_index := self.find_line_index(go_sub_line_id)) is not None:
                    self.subroutine_stack.append(
                        self.statement_index + 1
                    )  # Setup for RETURN.
                    self.statement_index = line_index
                else:
                    raise InterpreterError("No GOSUB line id.", self.current)

            case nodes.ReturnStatement():
                if not self.subroutine_stack:  # Check if the stack is empty.
                    raise InterpreterError("RETURN without GOSUB.", self.current)
                self.statement_index = self.subroutine_stack.pop()

            case nodes.PrintStatement(printables=printables):
                accumulated_string: str = ""
                for index, printable in enumerate(printables):
                    if index > 0:  # Put tabs between items in the list.
                        accumulated_string += "\t"

                    if isinstance(printable, nodes.NumericExpression):
                        accumulated_string += str(self.evaluate_numeric(printable))
                    else:  # Otherwise, it's a string.
                        accumulated_string += str(printable)

                print(accumulated_string)
                self.statement_index += 1

            case nodes.InputStatement(name=name):
                raw = input("? ").strip()
                try:
                    value = int(raw)
                except ValueError:
                    raise InterpreterError(
                        f"Expected numeric input for variable {name}. Got '{raw}'.",
                        self.current,
                    )

                self.variable_table[name] = value
                self.statement_index += 1

            case nodes.IfStatement(
                boolean_expr=boolean_expr, then_statement=then_statement
            ):
                if self.evaluate_boolean(boolean_expr):
                    self.interpret(then_statement)
                else:
                    self.statement_index += 1

            case _:
                raise InterpreterError(
                    f"Unexpected item {self.current} in statement list.", self.current
                )

    def evaluate_numeric(self, numeric_expression: nodes.NumericExpression) -> int:
        """Evaluates a numeric expression and returns its integer value.

        Args:
            numeric_expression: The numeric expression to evaluate.

        Returns:
            The integer value of the numeric expression.

        Raises:
            InterpreterError: If an error occurs during evaluation, such as an undefined variable
            or invalid operator.
        """
        match numeric_expression:
            case nodes.NumberLiteral(number=number):
                return number

            case nodes.VarRetrieve(name=name):
                if name in self.variable_table:
                    return self.variable_table[name]
                else:
                    raise InterpreterError(
                        f"Var {name} used before initialized.", numeric_expression
                    )

            case nodes.UnaryOperation(operator=operator, expr=expr):
                if operator is TokenType.MINUS:
                    return -self.evaluate_numeric(expr)
                else:
                    raise InterpreterError(
                        f"Expected - but got {operator}.", numeric_expression
                    )

            case nodes.BinaryOperation(
                operator=operator, left_expr=left, right_expr=right
            ):
                if operator is TokenType.PLUS:
                    return self.evaluate_numeric(left) + self.evaluate_numeric(right)
                elif operator is TokenType.MINUS:
                    return self.evaluate_numeric(left) - self.evaluate_numeric(right)
                elif operator is TokenType.MULTIPLY:
                    return self.evaluate_numeric(left) * self.evaluate_numeric(right)
                elif operator is TokenType.DIVIDE:
                    return self.evaluate_numeric(left) // self.evaluate_numeric(right)
                else:
                    InterpreterError(
                        f"Unexpected binary operator {operator}.", numeric_expression
                    )

            case _:
                raise InterpreterError(
                    "Expected numeric expression.", numeric_expression
                )

    def evaluate_boolean(self, boolean_expression: nodes.BooleanExpression) -> bool:
        """Evaluates a boolean expression and returns its boolean value.

        Args:
            boolean_expression: The boolean expression to evaluate.

        Returns:
            The boolean value of the boolean expression.

        Raises:
            InterpreterError: If an error occurs during evaluation, such as an invalid
            boolean operator.
        """
        left = self.evaluate_numeric(boolean_expression.left_expr)
        right = self.evaluate_numeric(boolean_expression.right_expr)

        match boolean_expression.operator:
            case TokenType.LESS:
                return left < right
            case TokenType.LESS_EQUAL:
                return left <= right
            case TokenType.GREATER:
                return left > right
            case TokenType.GREATER_EQUAL:
                return left >= right
            case TokenType.EQUAL:
                return left == right
            case TokenType.NOT_EQUAL:
                return left != right
            case _:
                raise InterpreterError(
                    f"Unexpected boolean operator {boolean_expression.operator}.",
                    boolean_expression,
                )
