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
        """Find the index of the matching bracket for the bracket at the given location.

        Args:
            start (int): The location of the bracket to find a match for.
            forward (bool): Whether to search forward (for "[") or backward (for "]").

        Returns:
            int: The location of the matching bracket, or the original location if no match was found.
        """
        in_between_brackets = 0
        direction = 1 if forward else -1
        location = start + direction
        start_bracket = "[" if forward else "]"
        end_bracket = "]" if forward else "["

        while 0 <= location < len(self.source_code):
            if self.source_code[location] == end_bracket:
                if not in_between_brackets:
                    return location
                in_between_brackets -= 1
            elif self.source_code[location] == start_bracket:
                in_between_brackets += 1
            location += direction

        # Didn't find a match.
        print(f"Error: could not find a match for {start_bracket} at {start}.")
        return start

    def clamp0_255_wraparound(self, num: int) -> int:
        """Simulate 8-bit unsigned integer overflow by clamping the given number to the range [0, 255] with wraparound.

        Args:
            num (int): The number to clamp.

        Returns:
            int: The clamped number.
        """
        if num > 255:
            return 0
        elif num < 0:
            return 255
        else:
            return num
