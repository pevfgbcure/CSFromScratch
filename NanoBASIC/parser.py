from typing import cast

from NanoBASIC.errors import ParserError
from NanoBASIC.nodes import (
    BooleanExpression,
    GoSubStatement,
    GoToStatement,
    IfStatement,
    LetStatement,
    NumericExpression,
    PrintStatement,
    ReturnStatement,
    Statement,
)
from NanoBASIC.tokenizer import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.token_index: int = 0

    @property
    def out_of_tokens(self) -> bool:
        return self.token_index >= len(self.tokens)

    @property
    def current(self) -> Token:
        if self.out_of_tokens:
            raise (ParserError(f"No tokens after {self.previous.kind}", self.previous))

        return self.tokens[self.token_index]

    @property
    def previous(self) -> Token:
        return self.tokens[self.token_index - 1]

    def consume(self, kind: TokenType) -> Token:
        if self.current.kind is kind:
            self.token_index += 1
            return self.previous

        raise ParserError(
            f"Expected {kind} after {self.previous} but got {self.current}.",
            self.current,
        )

    def parse(self) -> list[Statement]:
        statements: list[Statement] = []
        while not self.out_of_tokens:
            statement = self.parse_line()
            statements.append(statement)
        return statements

    def parse_line(self) -> Statement:
        number = self.consume(TokenType.NUMBER)
        return self.parse_statement(cast(int, number.associated_value))

    def parse_statement(self, line_id: int) -> Statement:
        match self.current.kind:
            case TokenType.PRINT:
                return self.parse_print(line_id)
            case TokenType.IF_T:
                return self.parse_if(line_id)
            case TokenType.LERT:
                return self.parse_let(line_id)
            case TokenType.GOTO:
                return self.parse_goto(line_id)
            case TokenType.GOSUB:
                return self.parse_gosub(line_id)
            case TokenType.RETURN_T:
                return self.parse_return(line_id)

        raise ParserError("Expected to find start of statement.", self.current)

    def parse_print(self, line_id: int) -> PrintStatement:
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
        return_token = self.consume(TokenType.RETURN_T)
        return ReturnStatement(
            line_id=line_id,
            line_num=return_token.line_num,
            col_start=return_token.col_start,
            col_end=return_token.col_end,
        )

    def parse_boolean_expression(self) -> BooleanExpression:
        pass

    def parse_numeric_expression(self) -> NumericExpression:
        pass
