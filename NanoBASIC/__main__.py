from argparse import ArgumentParser

from NanoBASIC.executioner import execute
from NanoBASIC.repl import interactive_repl

if __name__ == "__main__":
    # Parse the file argument (optional).
    file_parser = ArgumentParser("NanoBASIC")
    file_parser.add_argument(
        "basic_file",
        nargs="?",
        default=None,
        help="A text file containing NanoBASIC code. If omitted, enters interactive mode.",
    )
    arguments = file_parser.parse_args()

    if arguments.basic_file:
        execute(arguments.basic_file)
    else:
        interactive_repl()
