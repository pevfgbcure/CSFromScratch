import sys
import unittest
from io import StringIO
from pathlib import Path

from NanoBASIC.executioner import execute


def run(file_name: str | Path) -> str:
    """Tokenizes, parses, and interprets a NanoBASIC program; stores the output
    in a string and returns it.

    Args:
        file_name: The name of the NanoBASIC program to run.

    Returns:
        The output of the program as a string.
    """
    output_holder = StringIO()
    sys.stdout = output_holder
    execute(file_name)
    return output_holder.getvalue()


class NanoBASICTestCase(unittest.TestCase):
    """Tests for the NanoBASIC interpreter."""

    def setUp(self) -> None:
        """Set up the test case by defining the path to the folder containing
        example NanoBASIC programs.
        """
        self.example_folder = (
            Path(__file__).resolve().parent.parent / "NanoBASIC" / "Examples"
        )

    def test_print1(self):
        """Test the NanoBASIC interpreter by running a program that prints
        "Hello World".
        """
        program_output = run(self.example_folder / "print1.bas")
        expected = "Hello World\n"
        self.assertEqual(program_output, expected)

    def test_print2(self):
        """Test the NanoBASIC interpreter by running a program that demonstrates
        the use of variables and arithmetic operations.
        """
        program_output = run(self.example_folder / "print2.bas")
        expected = "4\n12\n30\n7\n100\t9\n"
        self.assertEqual(program_output, expected)

    def test_print3(self):
        """Test the NanoBASIC interpreter by running a program that demonstrates the
        use of variables, arithmetic operations, and string concatenation.
        """
        program_output = run(self.example_folder / "print3.bas")
        expected = "E is\t-31\n"
        self.assertEqual(program_output, expected)

    def test_variables(self):
        """Test the NanoBASIC interpreter by running a program that demonstrates the
        use of variables and arithmetic operations.
        """
        program_output = run(self.example_folder / "variables.bas")
        expected = "15\n"
        self.assertEqual(program_output, expected)

    def test_goto(self):
        """Test the NanoBASIC interpreter by running a program that demonstrates the
        use of the GOTO statement.
        """
        program_output = run(self.example_folder / "goto.bas")
        expected = "Josh\nDave\nNanoBASIC ROCKS\n"
        self.assertEqual(program_output, expected)

    def test_gosub(self):
        """Test the NanoBASIC interpreter by running a program that demonstrates the
        use of the GOSUB statement.
        """
        program_output = run(self.example_folder / "gosub.bas")
        expected = "10\n"
        self.assertEqual(program_output, expected)

    def test_if1(self):
        """Test the NanoBASIC interpreter by running a program that demonstrates the
        use of the IF statement.
        """
        program_output = run(self.example_folder / "if1.bas")
        expected = "10\n40\n50\n60\n70\n100\n"
        self.assertEqual(program_output, expected)

    def test_if2(self):
        """Test the NanoBASIC interpreter by running a program that demonstrates the
        use of the multiple IF-THEN statements on the same line.
        """
        program_output = run(self.example_folder / "if2.bas")
        expected = "GOOD\n"
        self.assertEqual(program_output, expected)

    def test_fib(self):
        """Test the NanoBASIC interpreter by running a program that calculates and
        prints the first Fibonacci numbers.
        """
        program_output = run(self.example_folder / "fib.bas")
        expected = "0\n1\n1\n2\n3\n5\n8\n13\n21\n34\n55\n89\n"
        self.assertEqual(program_output, expected)

    def test_factorial(self):
        """Test the NanoBASIC interpreter by running a program that calculates and
        prints the factorial of a number.
        """
        program_output = run(self.example_folder / "factorial.bas")
        expected = "120\n"
        self.assertEqual(program_output, expected)

    def test_print_with_escaped_quote(self):
        """Test that an escaped quote inside a string is interpreted correctly."""
        program_output = run(self.example_folder / "print_escaped_quote.bas")
        expected = 'He said "Hello World!"\n'
        self.assertEqual(program_output, expected)

    def test_gcd(self):
        """Test the NanoBASIC interpreter by running a program that calculates and
        prints the greatest common divisor of two numbers.
        """
        program_output = run(self.example_folder / "gcd.bas")
        expected = "7\n"
        self.assertEqual(program_output, expected)


if __name__ == "__main__":
    unittest.main()
