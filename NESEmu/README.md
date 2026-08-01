# NES Emulator

This is a simple NES emulator written in Python, with several limitations and not fully optimized for performance. It is intended for educational purposes and to demonstrate the basic concepts of emulation. It doesn't support all NES games and may have compatibility issues with certain ROMs.

## Project Structure

- `__main__.py`: Handles command line arguments and implements the main loop of the emulator.
- `rom.py`: Reads a ROM file and pretends to be a cartridge.
- `cpu.py`: Mantains CPU state, interprets instructions, and handles memory access.
- `ppu.py`: Implements the Picture Processing Unit (PPU) for rendering graphics.
