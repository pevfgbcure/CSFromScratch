from collections import deque

import NanoBASIC.nodes as nodes


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
        pass
