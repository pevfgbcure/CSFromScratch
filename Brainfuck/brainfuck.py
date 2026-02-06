from pathlib import Path


class Brainfuck:
    """A Brainfuck interpreter."""

    def __init__(self, file_name: str | Path):
        """Create a Brainfuck interpreter instance.

        Args:
            file_name (str | Path): The Brainfuck source code file to interpret.
        """
        # Open the text file and store it in an instace variable.
        with open(file_name, "r") as text_file:
            self.source_code: str = text_file.read()

    def execute(self):
        """Execute the Brainfuck source code stored in this instance."""
        # Setup state.
        cells: list[int] = [0] * 30_000
        cell_index = 0
        instruction_index = 0

        # Keep reading instructions as long as there are any left.
        while instruction_index < len(self.source_code):
            instruction = self.source_code[instruction_index]
            match instruction:
                case ">":
                    cell_index += 1
                case "<":
                    cell_index -= 1
                case "+":
                    cells[cell_index] = self.clamp0_255_wraparound(
                        cells[cell_index] + 1
                    )
                case "-":
                    cells[cell_index] = self.clamp0_255_wraparound(
                        cells[cell_index] - 1
                    )
                case ".":
                    print(chr(cells[cell_index]), end="", flush=True)
                case ",":
                    cells[cell_index] = self.clamp0_255_wraparound(int(input()))
                case "[":
                    if cells[cell_index] == 0:
                        instruction_index = self.find_bracket_match(
                            instruction_index, True
                        )
                case "]":
                    if cells[cell_index] != 0:
                        instruction_index = self.find_bracket_match(
                            instruction_index, False
                        )
            instruction_index += 1

    def find_bracket_match(self, start: int, forward: bool) -> int:
        pass

    def clamp0_255_wraparound(self, num: int) -> int:
        pass
