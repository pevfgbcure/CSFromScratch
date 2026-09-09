import unittest
from pathlib import Path

from NESEmu.cpu import CPU
from NESEmu.ppu import PPU
from NESEmu.rom import ROM


class CPUTestCase(unittest.TestCase):
    """Test cases for the NES CPU emulator."""

    def setUp(self) -> None:
        """Set up test environment."""
        self.test_folder = Path(__file__).resolve().parent.parent / "NESEmu" / "Tests"

    def test_nes_test(self):
        """Test the NES test ROM against the reference log."""
        # Create machinery that we are testing
        rom = ROM(self.test_folder / "nestest" / "nestest.nes")
        ppu = PPU(rom)
        cpu = CPU(ppu, rom)
        # Set up tests
        cpu.PC = 0xC000  # special starting location for tests
        with open(self.test_folder / "nestest" / "nestest.log") as f:
            correct_lines = f.readlines()
        log_line = 1
        # Check every line of the log against our own produced logs
        while log_line < 5260:  # go until first unofficial opcode test
            our_line = cpu.log()
            correct_line = correct_lines[log_line - 1]
            self.assertEqual(correct_line[0:14], our_line[0:14], f"PC/Opcode doesn't match at line {log_line}")
            self.assertEqual(correct_line[48:73], our_line[48:73], f"Registers don't match at line {log_line}")
            cpu.step()
            log_line += 1

    def test_blargg_instr_test_v5_basics(self):
        """Test the blargg instruction test - basics."""
        # Create machinery that we are testing
        rom = ROM(self.test_folder / "instr_test-v5" / "rom_singles" / "01-basics.nes")
        ppu = PPU(rom)
        cpu = CPU(ppu, rom)
        # Tests run as long as 0x6000 is 80, and then 0x6000 is result code; 0 means success
        rom.prg_ram[0] = 0x80
        while rom.prg_ram[0] == 0x80:  # go until first unofficial opcode test
            cpu.step()
        self.assertEqual(0, rom.prg_ram[0], f"Result code of basics test is {rom.prg_ram[0]} not 0")
        message = bytes(rom.prg_ram[4:]).decode("utf-8")
        print(message[0 : message.index("\0")])  # message ends with null terminator

    def test_blargg_instr_test_v5_implied(self):
        """Test the blargg instruction test - implied."""
        # Create machinery that we are testing
        rom = ROM(self.test_folder / "instr_test-v5" / "rom_singles" / "02-implied.nes")
        ppu = PPU(rom)
        cpu = CPU(ppu, rom)
        # Tests run as long as 0x6000 is 80, and then 0x6000 is result code; 0 means success
        rom.prg_ram[0] = 0x80
        while rom.prg_ram[0] == 0x80:  # go until first unofficial opcode test
            cpu.step()
        self.assertEqual(0, rom.prg_ram[0], f"Result code of implied test is {rom.prg_ram[0]} not 0")
        message = bytes(rom.prg_ram[4:]).decode("utf-8")
        print(message[0 : message.index("\0")])  # message ends with null terminator

    def test_blargg_instr_test_v5_branches(self):
        """Test the blargg instruction test - branches."""
        # Create machinery that we are testing
        rom = ROM(self.test_folder / "instr_test-v5" / "rom_singles" / "10-branches.nes")
        ppu = PPU(rom)
        cpu = CPU(ppu, rom)
        # Tests run as long as 0x6000 is 80, and then 0x6000 is result code; 0 means success
        rom.prg_ram[0] = 0x80
        while rom.prg_ram[0] == 0x80:  # go until first unofficial opcode test
            cpu.step()
        self.assertEqual(0, rom.prg_ram[0], f"Result code of braches test is {rom.prg_ram[0]} not 0")
        message = bytes(rom.prg_ram[4:]).decode("utf-8")
        print(message[0 : message.index("\0")])  # message ends with null terminator

    def test_blargg_instr_test_v5_stack(self):
        """Test the blargg instruction test - stack."""
        # Create machinery that we are testing
        rom = ROM(self.test_folder / "instr_test-v5" / "rom_singles" / "11-stack.nes")
        ppu = PPU(rom)
        cpu = CPU(ppu, rom)
        # Tests run as long as 0x6000 is 80, and then 0x6000 is result code; 0 means success
        rom.prg_ram[0] = 0x80
        while rom.prg_ram[0] == 0x80:  # go until first unofficial opcode test
            cpu.step()
        self.assertEqual(0, rom.prg_ram[0], f"Result code of stack test is {rom.prg_ram[0]} not 0")
        message = bytes(rom.prg_ram[4:]).decode("utf-8")
        print(message[0 : message.index("\0")])  # message ends with null terminator

    def test_blargg_instr_test_v5_jmp_jsr(self):
        """Test the blargg instruction test - jmp/jsr."""
        # Create machinery that we are testing
        rom = ROM(self.test_folder / "instr_test-v5" / "rom_singles" / "12-jmp_jsr.nes")
        ppu = PPU(rom)
        cpu = CPU(ppu, rom)
        # Tests run as long as 0x6000 is 80, and then 0x6000 is result code; 0 means success
        rom.prg_ram[0] = 0x80
        while rom.prg_ram[0] == 0x80:  # go until first unofficial opcode test
            cpu.step()
        self.assertEqual(0, rom.prg_ram[0], f"Result code of jmp_jsr test is {rom.prg_ram[0]} not 0")
        message = bytes(rom.prg_ram[4:]).decode("utf-8")
        print(message[0 : message.index("\0")])  # message ends with null terminator

    def test_blargg_instr_test_v5_rts(self):
        """Test the blargg instruction test - rts."""
        # Create machinery that we are testing
        rom = ROM(self.test_folder / "instr_test-v5" / "rom_singles" / "13-rts.nes")
        ppu = PPU(rom)
        cpu = CPU(ppu, rom)
        # Tests run as long as 0x6000 is 80, and then 0x6000 is result code; 0 means success
        rom.prg_ram[0] = 0x80
        while rom.prg_ram[0] == 0x80:  # go until first unofficial opcode test
            cpu.step()
        self.assertEqual(0, rom.prg_ram[0], f"Result code of rts test is {rom.prg_ram[0]} not 0")
        message = bytes(rom.prg_ram[4:]).decode("utf-8")
        print(message[0 : message.index("\0")])  # message ends with null terminator

    def test_blargg_instr_test_v5_rti(self):
        """Test the blargg instruction test - rti."""
        # Create machinery that we are testing
        rom = ROM(self.test_folder / "instr_test-v5" / "rom_singles" / "14-rti.nes")
        ppu = PPU(rom)
        cpu = CPU(ppu, rom)
        # Tests run as long as 0x6000 is 80, and then 0x6000 is result code; 0 means success
        rom.prg_ram[0] = 0x80
        while rom.prg_ram[0] == 0x80:  # go until first unofficial opcode test
            cpu.step()
        self.assertEqual(0, rom.prg_ram[0], f"Result code of rti test is {rom.prg_ram[0]} not 0")
        message = bytes(rom.prg_ram[4:]).decode("utf-8")
        print(message[0 : message.index("\0")])  # message ends with null terminator

    def test_blargg_instr_test_v5_brk(self):
        """Test the blargg instruction test - brk."""
        # Create machinery that we are testing
        rom = ROM(self.test_folder / "instr_test-v5" / "rom_singles" / "15-brk.nes")
        ppu = PPU(rom)
        cpu = CPU(ppu, rom)
        # Tests run as long as 0x6000 is 80, and then 0x6000 is result code; 0 means success
        rom.prg_ram[0] = 0x80
        while rom.prg_ram[0] == 0x80:  # go until first unofficial opcode test
            cpu.step()
        message = bytes(rom.prg_ram[4:]).decode("utf-8")
        print(message[0 : message.index("\0")])  # message ends with null terminator
        self.assertEqual(0, rom.prg_ram[0], f"Result code of brk test is {rom.prg_ram[0]} not 0")

    def test_blargg_instr_test_v5_special(self):
        """Test the blargg instruction test - special."""
        # Create machinery that we are testing
        rom = ROM(self.test_folder / "instr_test-v5" / "rom_singles" / "16-special.nes")
        ppu = PPU(rom)
        cpu = CPU(ppu, rom)
        # Tests run as long as 0x6000 is 80, and then 0x6000 is result code; 0 means success
        rom.prg_ram[0] = 0x80
        while rom.prg_ram[0] == 0x80:  # go until first unofficial opcode test
            cpu.step()
        message = bytes(rom.prg_ram[4:]).decode("utf-8")
        print(message[0 : message.index("\0")])  # message ends with null terminator
        self.assertEqual(0, rom.prg_ram[0], f"Result code of special test is {rom.prg_ram[0]} not 0")


if __name__ == "__main__":
    unittest.main()
