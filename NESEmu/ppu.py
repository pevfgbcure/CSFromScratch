from array import array

import numpy as np

from NESEmu.rom import ROM

# IMPORTANT CONSTANTS.
SPR_RAM_SIZE = 256
NAMETABLE_SIZE = 2048
PALETTE_SIZE = 32
NES_WIDTH = 256
NES_HEIGHT = 240
NES_PALETTE = [
    0x7C7C7C,
    0x0000FC,
    0x0000BC,
    0x4428BC,
    0x940084,
    0xA80020,
    0xA81000,
    0x881400,
    0x503000,
    0x007800,
    0x006800,
    0x005800,
    0x004058,
    0x000000,
    0x000000,
    0x000000,
    0xBCBCBC,
    0x0078F8,
    0x0058F8,
    0x6844FC,
    0xD800CC,
    0xE40058,
    0xF83800,
    0xE45C10,
    0xAC7C00,
    0x00B800,
    0x00A800,
    0x00A844,
    0x008888,
    0x000000,
    0x000000,
    0x000000,
    0xF8F8F8,
    0x3CBCFC,
    0x6888FC,
    0x9878F8,
    0xF878F8,
    0xF85898,
    0xF87858,
    0xFCA044,
    0xF8B800,
    0xB8F818,
    0x58D854,
    0x58F898,
    0x00E8D8,
    0x787878,
    0x000000,
    0x000000,
    0xFCFCFC,
    0xA4E4FC,
    0xB8B8F8,
    0xD8B8F8,
    0xF8B8F8,
    0xF8A4C0,
    0xF0D0B0,
    0xFCE0A8,
    0xF8D878,
    0xD8F878,
    0xB8F8B8,
    0xB8F8D8,
    0x00FCFC,
    0xF8D8F8,
    0x000000,
    0x000000,
]


class PPU:
    """NES Picture Processing Unit emulator."""

    def __init__(self, rom: ROM) -> None:
        """Initialize the PPU with the given ROM.

        Args:
            rom: The ROM containing the game data.
        """
        self.rom: ROM = rom
        # PPU memory.
        self.spr: array[int] = array("B", [0] * SPR_RAM_SIZE)  # sprite RAM
        self.nametables: array[int] = array("B", [0] * NAMETABLE_SIZE)  # nametable RAM
        self.palette: array[int] = array("B", [0] * PALETTE_SIZE)  # palette RAM
        # Registers.
        self.addr: int = 0  # main PPU address register
        self.addr_write_latch: bool = False
        self.status: int = 0
        self.spr_address: int = 0
        # Variables controlled by PPU control registers.
        self.nametable_address: int = 0
        self.address_increment: int = 1
        self.spr_pattern_table_address: int = 0
        self.background_pattern_table_address: int = 0
        self.generate_nmi: bool = False
        self.show_background: bool = False
        self.show_sprites: bool = False
        self.left_8_sprite_show: bool = False
        self.left_8_background_show: bool = False
        # Internal helper variables
        self.buffer2007: int = 0
        self.scanline: int = 0
        self.cycle: int = 0
        # Pixels for screen
        self.display_buffer: np.ndarray = np.zeros((NES_WIDTH, NES_HEIGHT), dtype=np.uint32)

    def step(self):
        """
        Execute one PPU cycle.

        Handles background and sprite drawing during the visible scanlines,
        sets VBlank status flags at the appropriate times, and updates the
        scanline and cycle counters.
        """
        # A simplified PPU (only draws once per frame).
        if (self.scanline == 240) and (self.cycle == 256):
            if self.show_background:
                self.draw_background()
            if self.show_sprites:
                self.draw_sprites(False)
        if (self.scanline == 241) and (self.cycle == 1):
            self.status |= 0b10000000  # set vblank
        if (self.scanline == 261) and (self.cycle == 1):
            # Vblank off, clear sprite zero, clear sprite overflow
            self.status |= 0b00011111

        self.cycle += 1
        if self.cycle > 340:
            self.cycle = 0
            self.scanline += 1
            if self.scanline > 261:
                self.scanline = 0

    def draw_background(self):
        """
        Draw the background tiles from nametables to the display buffer.

        This method iterates through the nametable entries, reads tile indices,
        applies palette attributes from the attribute table, and renders each
        tile's pixel data to the display buffer using the NES palette.
        """
        attribute_table_address = self.nametable_address + 960
        for y in range(30):
            for x in range(32):
                tile_address = self.nametable_address + y * 32 + x
                nametable_entry = self.read_memory(tile_address)
                attr_x = x // 4
                attr_y = x // 4
                attribute_address = attribute_table_address + attr_y * 8 + attr_x
                attribute_entry = self.read_memory(attribute_address)
                block = (y & 0x02) | ((x & 0x02) >> 1)
                attribute_bits = 0
                if block == 0:
                    attribute_bits = (attribute_entry & 0b00000011) << 2
                elif block == 1:
                    attribute_bits = attribute_entry & 0b00001100
                elif block == 2:
                    attribute_bits = (attribute_entry & 0b00110000) >> 2
                elif block == 3:
                    attribute_bits = (attribute_entry & 0b11000000) >> 4
                else:
                    print("Invalid block")

                for fine_y in range(8):
                    low_order = self.read_memory(self.background_pattern_table_address + nametable_entry * 16 + fine_y)
                    high_order = self.read_memory(
                        self.background_pattern_table_address + nametable_entry * 16 + 8 + fine_y
                    )
                    for fine_x in range(8):
                        pixel = (
                            ((low_order >> (7 - fine_x)) & 1)
                            | (((high_order >> (7 - fine_x)) & 1) << 1)
                            | attribute_bits
                        )
                        x_screen_loc = x * 8 + fine_x
                        y_screen_loc = y * 8 + fine_y
                        transparent = (pixel & 3) == 0
                        # If the background is transparent, use the first color in the palette.
                        color = self.palette[0] if transparent else self.palette[pixel]
                        self.display_buffer[x_screen_loc, y_screen_loc] = NES_PALETTE[color]

    def draw_sprites(self, background_transparent: bool):
        pass
