from __future__ import annotations

from array import array
from dataclasses import dataclass
from enum import Enum
from typing import Callable

from NESEmu.ppu import PPU, SPR_RAM_SIZE

from NESEmu.rom import ROM

# List various memory access schemes used by the 6502 CPU.
MemMode = Enum(
    "MemMode",
    "DUMMY ABSOLUTE ABSOLUTE_X ABSOLUTE_Y ACCUMULATOR "
    "IMMEDIATE IMPLIED INDEXED_INDIRECT INDIRECT "
    "INDIRECT_INDEXED RELATIVE ZEROPAGE ZEROPAGE_X "
    "ZEROPAGE_Y",
)

# List all the instructions in the 6502 CPU instruction set. Even the ones we won't implement.
InstructionType = Enum(
    "InstructionType",
    "ADC AHX ALR ANC AND ARR ASL AXS "
    "BCC BCS BEQ BIT BMI BNE BPL BRK "
    "BVC BVS CLC CLD CLI CLV CMP CPX "
    "CPY DCP DEC DEX DEY EOR INC INX "
    "INY ISC JMP JSR KIL LAS LAX LDA "
    "LDX LDY LSR NOP ORA PHA PHP PLA "
    "PLP RLA ROL ROR RRA RTI RTS SAX "
    "SBC SEC SED SEI SHX SHY SLO SRE "
    "STA STX STY TAS TAX TAY TSX TXA "
    "TXS TYA XAA",
)


@dataclass(frozen=True)
class Instruction:
    """Represents a single instruction in the 6502 CPU instruction set."""

    type: InstructionType
    method: Callable[[Instruction, int], None]
    mode: MemMode
    length: int
    ticks: int
    page_ticks: int


@dataclass
class Joypad:
    """Represents the NES gamepad."""

    strobe: bool = False
    read_count: int = 0
    a: bool = False
    b: bool = False
    select: bool = False
    start: bool = False
    up: bool = False
    down: bool = False
    left: bool = False
    right: bool = False


STACK_POINTER_RESET = 0xFD
STACK_START = 0x100
RESET_VECTOR = 0xFFFC
NMI_VECTOR = 0xFFFA
IRQ_BRK_VECTOR = 0xFFFE
MEM_SIZE = 2048
