from pathlib import Path

from NanoBASIC.interpreter import Interpreter
from NanoBASIC.parser import Parser
from NanoBASIC.tokenizer import tokenize


def execute(file_name: str | Path):
    """Loads a NanoBASIC file and tokenizes, parses, and executes it.

    Args:
        file_name (str | Path): The name of the NanoBASIC file to execute.
    """
    with open(file_name, "r") as text_file:
        tokens = tokenize(text_file)
        ast = Parser(tokens).parse()
        Interpreter(ast).run()
