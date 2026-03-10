from typing import cast

from NanoBASIC.errors import ParserError
from NanoBASIC.nodes import (
    BinaryOperation,
    BooleanExpression,
    GoSubStatement,
    GoToStatement,
    IfStatement,
    LetStatement,
    NumberLiteral,
    NumericExpression,
    PrintStatement,
    ReturnStatement,
    Statement,
    UnaryOperation,
    VarRetrieve,
)
from NanoBASIC.tokenizer import Token, TokenType


class Parser:
    """Parser for NanoBASIC. Takes in a list of tokens and produces an AST."""

    def __init__(self, tokens: list[Token]):
        """Initialize the parser with a list of tokens.

        Args:
            tokens: The list of tokens to parse.
        """
        self.tokens = tokens
        self.token_index: int = 0

    @property
    def out_of_tokens(self) -> bool:
        """Whether the parser has reached the end of the token list."""
        return self.token_index >= len(self.tokens)

    @property
    def current(self) -> Token:
        """The current token being parsed."""
        if self.out_of_tokens:
            raise (ParserError(f"No tokens after {self.previous.kind}", self.previous))

        return self.tokens[self.token_index]

    @property
    def previous(self) -> Token:
        """The most recently consumed token."""
        return self.tokens[self.token_index - 1]

    def consume(self, kind: TokenType) -> Token:
        """Consume the current token if it is of the expected kind, otherwise raise
        an error.

        Args:
            kind: The expected kind of the current token.

        Returns:
            The consumed token.

        Raises:
            ParserError: If the current token is not of the expected kind.
        """
        if self.current.kind is kind:
            self.token_index += 1
            return self.previous

        raise ParserError(
            f"Expected {kind} after {self.previous} but got {self.current}.",
            self.current,
        )

    def parse(self) -> list[Statement]:
        """Parse the list of tokens into an AST.

        Returns:
            The list of statements in the program.
        """
        statements: list[Statement] = []
        while not self.out_of_tokens:
            statement = self.parse_line()
            statements.append(statement)
        return statements

    def parse_line(self) -> Statement:
        """Parse a line of the program, which starts with a line number and is
        followed by a statement.

        Returns:
            The statement on the line.
        """
        number = self.consume(TokenType.NUMBER)
        return self.parse_statement(cast(int, number.associated_value))

    def parse_statement(self, line_id: int) -> Statement:
        match self.current.kind:
            case TokenType.PRINT:
                return self.parse_print(line_id)
            case TokenType.IF_T:
                return self.parse_if(line_id)
            case TokenType.LET:
                return self.parse_let(line_id)
            case TokenType.GOTO:
                return self.parse_goto(line_id)
            case TokenType.GOSUB:
                return self.parse_gosub(line_id)
            case TokenType.RETURN_T:
                return self.parse_return(line_id)

        raise ParserError("Expected to find start of statement.", self.current)

    def parse_print(self, line_id: int) -> PrintStatement:
        """Parse a print statement, which consists of the PRINT keyword followed by a list
        of strings and numeric expressions to print, separated by commas.

        Returns:
            The parsed PrintStatement.

        Raises:
            ParserError: If the print statement is not well-formed, such as if it contains
            something other than strings and numeric expressions.
        """
        print_token = self.consume(TokenType.PRINT)
        printables: list[str | NumericExpression] = []
        last_col: int = print_token.col_end

        while True:  # Keep finding things to print.
            if self.current.kind is TokenType.STRING:
                string = self.consume(TokenType.STRING)
                printables.append(cast(str, string.associated_value))
                last_col = string.col_end
            elif (expression := self.parse_numeric_expression()) is not None:
                printables.append(expression)
                last_col = expression.col_end
            else:
                raise ParserError(
                    "Only strings and numeric expressions are allowed in print list.",
                    self.current,
                )

            if not self.out_of_tokens and self.current.kind is TokenType.COMMA:
                self.consume(TokenType.COMMA)
                continue

            break

        return PrintStatement(
            line_id=line_id,
            line_num=print_token.line_num,
            col_start=print_token.col_start,
            col_end=last_col,
            printables=printables,
        )

    def parse_if(self, line_id: int) -> IfStatement:
        """Parse an if statement, which consists of the IF keyword followed by a boolean expression,
        the THEN keyword, and a statement to execute if the boolean expression is true.

        Returns:
            The parsed IfStatement.
        """
        if_token = self.consume(TokenType.IF_T)
        boolean_expression = self.parse_boolean_expression()
        self.consume(TokenType.THEN)
        statement = self.parse_statement(line_id)
        return IfStatement(
            line_id=line_id,
            line_num=if_token.line_num,
            col_start=if_token.col_start,
            col_end=statement.col_end,
            boolean_expr=boolean_expression,
            then_statement=statement,
        )

    def parse_let(self, line_id: int) -> LetStatement:
        """Parse a let statement, which consists of the LET keyword followed by a variable name, an equal sign,
        and a numeric expression to assign to the variable.

        Returns:
            The parsed LetStatement.
        """
        let_token = self.consume(TokenType.LET)
        variable = self.consume(TokenType.VARIABLE)
        self.consume(TokenType.EQUAL)
        expression = self.parse_numeric_expression()
        return LetStatement(
            line_id=line_id,
            line_num=let_token.line_num,
            col_start=let_token.col_start,
            col_end=expression.col_end,
            name=cast(str, variable.associated_value),
            expr=expression,
        )

    def parse_goto(self, line_id: int) -> GoToStatement:
        """Parse a goto statement, which consists of the GOTO keyword followed by a numeric expression
        representing the line number to jump to.

        Returns:
            The parsed GoToStatement.
        """
        goto_token = self.consume(TokenType.GOTO)
        expression = self.parse_numeric_expression()
        return GoToStatement(
            line_id=line_id,
            line_num=goto_token.line_num,
            col_start=goto_token.col_start,
            col_end=expression.col_end,
            line_expr=expression,
        )

    def parse_gosub(self, line_id: int) -> GoSubStatement:
        """Parse a gosub statement, which consists of the GOSUB keyword followed by a numeric expression
        representing the line number to jump to.

        Returns:
            The parsed GoSubStatement.
        """
        gosub_token = self.consume(TokenType.GOSUB)
        expression = self.parse_numeric_expression()
        return GoSubStatement(
            line_id=line_id,
            line_num=gosub_token.line_num,
            col_start=gosub_token.col_start,
            col_end=expression.col_end,
            line_expr=expression,
        )

    def parse_return(self, line_id: int) -> ReturnStatement:
        """Parse a return statement, which consists of the RETURN keyword.

        Returns:
            The parsed ReturnStatement.
        """
        return_token = self.consume(TokenType.RETURN_T)
        return ReturnStatement(
            line_id=line_id,
            line_num=return_token.line_num,
            col_start=return_token.col_start,
            col_end=return_token.col_end,
        )

    def parse_boolean_expression(self) -> BooleanExpression:
        """Parse a boolean expression, which consists of two numeric expressions separated
        by a boolean operator.

        Returns:
            The parsed BooleanExpression.

        Raises:
            ParserError: If the boolean expression is not well-formed, such as if it does
            not contain a boolean operator.
        """
        left = self.parse_numeric_expression()
        if self.current.kind in {
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
            TokenType.NOT_EQUAL,
        }:
            operator = self.consume(self.current.kind)
            right = self.parse_numeric_expression()
            return BooleanExpression(
                line_num=left.line_num,
                col_start=left.col_start,
                col_end=right.col_end,
                operator=operator.kind,
                left_expr=left,
                right_expr=right,
            )

        raise ParserError(
            f"Expected boolean operator but found {self.current.kind}.", self.current
        )

    def parse_numeric_expression(self) -> NumericExpression:
        """Parse a numeric expression, which consists of terms separated by '+' and '-'.

        Returns:
             The parsed NumericExpression.
        """
        left = self.parse_term()
        # Keep parsing +s and -s until there are no more
        while True:
            if self.out_of_tokens:  # What if expression is end of file?
                return left

            if self.current.kind is TokenType.PLUS:
                self.consume(TokenType.PLUS)
                right = self.parse_term()
                left = BinaryOperation(
                    line_num=left.line_num,
                    col_start=left.col_start,
                    col_end=right.col_end,
                    operator=TokenType.PLUS,
                    left_expr=left,
                    right_expr=right,
                )
            elif self.current.kind is TokenType.MINUS:
                self.consume(TokenType.MINUS)
                right = self.parse_term()
                left = BinaryOperation(
                    line_num=left.line_num,
                    col_start=left.col_start,
                    col_end=right.col_end,
                    operator=TokenType.MINUS,
                    left_expr=left,
                    right_expr=right,
                )
            else:
                break  # No more, must be end of expression.

        return left

    def parse_term(self) -> NumericExpression:
        """Parse a term, which consists of factors separated by '*' and '/'.

        Returns:
            The parsed NumericExpression.
        """
        left = self.parse_factor()
        # Keep parsing *s and /s until there are no more.
        while True:
            if self.out_of_tokens:  # What if expression is end of file?
                return left

            if self.current.kind is TokenType.MULTIPLY:
                self.consume(TokenType.MULTIPLY)
                right = self.parse_factor()
                left = BinaryOperation(
                    line_num=left.line_num,
                    col_start=left.col_start,
                    col_end=right.col_end,
                    operator=TokenType.MULTIPLY,
                    left_expr=left,
                    right_expr=right,
                )
            elif self.current.kind is TokenType.DIVIDE:
                self.consume(TokenType.DIVIDE)
                right = self.parse_factor()
                left = BinaryOperation(
                    line_num=left.line_num,
                    col_start=left.col_start,
                    col_end=right.col_end,
                    operator=TokenType.DIVIDE,
                    left_expr=left,
                    right_expr=right,
                )
            else:
                break  # No more, must be end of expression.

        return left

    def parse_factor(self) -> NumericExpression:
        """Parse a factor, which could be a variable, a number, a parenthesized expression, or a unary minus.

        Returns:
            The parsed NumericExpression.

        Raises:
            ParserError: If the factor is not well-formed, such as if it is an unexpected token.
        """
        if self.current.kind is TokenType.VARIABLE:
            variable = self.consume(TokenType.VARIABLE)
            return VarRetrieve(
                line_num=variable.line_num,
                col_start=variable.col_start,
                col_end=variable.col_end,
                name=cast(str, variable.associated_value),
            )
        elif self.current.kind is TokenType.NUMBER:
            number = self.consume(TokenType.NUMBER)
            return NumberLiteral(
                line_num=number.line_num,
                col_start=number.col_start,
                col_end=number.col_end,
                number=int(cast(str, number.associated_value)),
            )
        elif self.current.kind is TokenType.OPEN_PAREN:
            self.consume(TokenType.OPEN_PAREN)
            expression = self.parse_numeric_expression()
            if self.current.kind is not TokenType.CLOSE_PAREN:
                raise ParserError("Expected matching close parenthesis.", self.current)
            self.consume(TokenType.CLOSE_PAREN)
            return expression
        elif self.current.kind is TokenType.MINUS:
            minus = self.consume(TokenType.MINUS)
            expression = self.parse_factor()
            return UnaryOperation(
                line_num=minus.line_num,
                col_start=minus.col_start,
                col_end=expression.col_end,
                operator=TokenType.MINUS,
                expr=expression,
            )
        raise ParserError("Unexpected token in numeric expression.", self.current)
