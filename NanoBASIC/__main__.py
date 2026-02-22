from argparse import ArgumentParser

from NanoBASIC.executioner import execute

if __name__ == "__main__":
    # Parse the file argument.
    file_parser = ArgumentParser("NanoBASIC")
    file_parser.add_argument(
        "basic_file", help="A text file containing NanoBASIC code."
    )
    arguments = file_parser.parse_args()
    execute(arguments.basic_file)
