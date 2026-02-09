import sys
import unittest
from io import StringIO
from pathlib import Path

from Brainfuck.brainfuck import Brainfuck


def run(file_name: str | Path) -> str:
    """Tokenizes, parses, and interprets a Brainfuck program; stores the output
    in a string and returns it.

    Args:
        file_name (str | Path): The Brainfuck source code file to interpret.

    Returns:
        str: The output of the Brainfuck program.
    """
    output_holder = StringIO()
    sys.stdout = output_holder
    Brainfuck(file_name).execute()
    return output_holder.getvalue()


class BrainfuckTestCase(unittest.TestCase):
    """Tests for the Brainfuck interpreter."""

    def setUp(self) -> None:
        """Set up the test case by defining the path to the folder containing example Brainfuck programs."""
        self.example_folder = (
            Path(__file__).resolve().parent.parent / "Brainfuck" / "examples"
        )

    def test_hello_world(self):
        """Test the Brainfuck interpreter by running a verbose "Hello World!" program."""
        program_output = run(self.example_folder / "hello_world_verbose.bf")
        expected = "Hello World!\n"
        self.assertEqual(program_output, expected)

    def test_fibonacci(self):
        """Test the Brainfuck interpreter by running a program that prints the first 11 Fibonacci numbers."""
        program_output = run(self.example_folder / "fibonacci.bf")
        expected = "1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89"
        self.assertEqual(program_output, expected)

    def test_cell_size(self):
        """Test the Brainfuck interpreter by running a program that demonstrates that the cells are 8 bits in size."""
        program_output = run(self.example_folder / "cell_size.bf")
        expected = "8 bit cells\n"
        self.assertEqual(program_output, expected)

    def test_beer(self):
        """Test the Brainfuck interpreter by running a program that prints the lyrics to "99 Bottles of Beer on the Wall"."""
        program_output = run(self.example_folder / "beer.bf")
        with open(self.example_folder / "beer.out", "r") as file:
            expected = file.read()
            self.assertEqual(program_output, expected)


if __name__ == "__main__":
    unittest.main()
