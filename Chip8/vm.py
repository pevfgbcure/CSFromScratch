from array import array

import numpy as np

from Chip8.constants import (
    BLACK,
    FONT_SET,
    RAM_SIZE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SPRITE_WIDTH,
    WHITE,
)


def concat_nibbles(*args: int) -> int:
    """Concatenate the given nibbles into a single integer.
    This makes it easier to work with the 4-bit nibbles that are used in CHIP-8 instructions.

    Args:
        *args (int): The nibbles to concatenate.

    Returns:
        int: The concatenated integer.
    """
    result = 0
    for arg in args:
        result = (result << 4) | arg
    return result


class VM:
    """A virtual machine that emulates the CHIP-8 architecture."""

    def __init__(self, program_data: bytes):
        """Initialize the virtual machine with its initial state and load the program data into memory."""
        # General Purpose Registers (CHIP-8 has 16 of these registers).
        self.v = array("B", [0] * 16)
        # Index Register.
        self.i = 0
        # Program Counter (stars at 0x200 because addresses below that were
        #   used for the VM itself in the original CHIP-8).
        self.pc = 0x200
        # Memory (the standard 4k on the original CHIP-8).
        self.ram = array("B", [0] * RAM_SIZE)
        # Load the font set into the first 80 bytes.
        self.ram[0 : len(FONT_SET)] = array("B", FONT_SET)
        # Copy program into RAM starting at byte 512 by convention.
        self.ram[512 : (512 + len(program_data))] = array("B", program_data)
        # Stack (in real hardware this is typically limited to 12 or 16
        #   PC addresses for jumps, but since this will run in modern hardware
        #   it can expand/contract as needed).
        self.stack = []
        # Graphics buffer for the screen (64 x 32 pixels).
        self.display_buffer = np.zeros((SCREEN_WIDTH, SCREEN_HEIGHT), dtype=np.uint32)
        self.needs_redraw = False
        # Timers (simple registers that count down to 0 at 60 Hz).
        self.delay_timer = 0
        self.sound_timer = 0
        # These hold the status of physical keys being pressed down on the keyboard.
        self.keys = [False] * 16  # CHIP-8 has 16 keys

    def decrement_timers(self):
        """Decrement the delay and sound timers if they are greater than 0."""
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1

    @property
    def play_sound(self) -> bool:
        """Return True if the sound timer is greater than 0, indicating that a sound should be played."""
        return self.sound_timer > 0

    def draw_sprite(self, x: int, y: int, height: int):
        """Draw a sprite at the given (x, y) coordinates with the specified height.
        The sprite data is read from memory starting at the address in the index register (self.i).

        Args:
            x (int): The x-coordinate where the sprite will be drawn.
            y (int): The y-coordinate where the sprite will be drawn.
            height (int): The height of the sprite in pixels (number of rows).
        """
        flipped_black = False  # did drawing this flip any pixels?
        for row in range(0, height):
            row_bits = self.ram[self.i + row]
            for col in range(0, SPRITE_WIDTH):
                px = x + col
                py = y + row
                if px >= SCREEN_WIDTH or py >= SCREEN_HEIGHT:
                    continue  # ignore off-screen pixels
                new_bit = (row_bits >> (7 - col)) & 1
                old_bit = self.display_buffer[px, py] & 1
                if new_bit & old_bit:  # if both set, flip white to black
                    flipped_black = True
                # CHIP-8 draws by XORing.
                new_pixel = new_bit ^ old_bit
                self.display_buffer[px, py] = WHITE if new_pixel else BLACK
        # Set flipped flag for collision detection.
        self.v[0xF] = 1 if flipped_black else 0
