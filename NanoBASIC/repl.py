from io import StringIO
from typing import cast

import NanoBASIC.nodes as nodes
from NanoBASIC.errors import InterpreterError, ParserError
from NanoBASIC.interpreter import Interpreter
from NanoBASIC.parser import Parser
from NanoBASIC.tokenizer import TokenType, tokenize


def interactive_repl():
    """Runs an interactive REPL for NanoBASIC with CLEAR, LIST, RUN, and END commands."""
    stored_statements: dict[int, tuple[nodes.Statement, str]] = {}

    print("NanoBASIC Interactive Mode")
    print(
        "Commands: CLEAR (clear program), LIST (list program), RUN (run program), END (exit)"
    )
    print()

    while True:
        try:
            user_input = input("> ").strip()

            if not user_input:
                continue

            # Check if input is a command.
            command = user_input.upper()

            if command == "END":
                print("Exiting NanoBASIC.")
                break
            elif command == "CLEAR":
                stored_statements.clear()
                print("Program cleared.")
            elif command == "LIST":
                if not stored_statements:
                    print("(empty)")
                else:
                    for line_id in sorted(stored_statements.keys()):
                        stmt = stored_statements[line_id][1]
                        print(stmt)
            elif command == "RUN":
                if not stored_statements:
                    print("No program to run.")
                else:
                    try:
                        # Sort by line_id and create interpreter.
                        sorted_stmts = [
                            stored_statements[line_id][0]
                            for line_id in sorted(stored_statements.keys())
                        ]
                        interpreter = Interpreter(sorted_stmts)
                        interpreter.run()
                    except InterpreterError as e:
                        print(f"Runtime error: {e}")
            else:
                # Try to parse as a program line (must start with a number).
                tokens_list = tokenize(StringIO(user_input))

                if not tokens_list:
                    print("Empty input.")
                    continue

                # Check if first token is a number.
                first_token = tokens_list[0]
                if first_token.kind != TokenType.NUMBER:
                    print(f"Unknown command: {user_input}")
                    continue

                # Parse the line as a program statement.
                try:
                    line_id = cast(int, first_token.associated_value)
                    # Create a parser with the tokens and parse the statement.
                    parser = Parser(tokens_list)
                    parser.consume(TokenType.NUMBER)  # Consume the line number token.
                    statement = parser.parse_statement(line_id)
                    stored_statements[line_id] = (statement, user_input)
                except ParserError as e:
                    print(f"Parse error: {e}")

        except EOFError:
            print()
            print("Exiting NanoBASIC.")
            break
        except KeyboardInterrupt:
            print()
            print("Exiting NanoBASIC.")
            break
