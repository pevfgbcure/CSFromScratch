import unittest
from array import array

from RetroDither.macpaint import run_length_encode


class RetroDitherTestCase(unittest.TestCase):
    # Example from
    # web​.­archive​.­org​/­web​/­20080705155158​/­http://­developer​.­apple​.­com​/­technotes​/­tn​/­tn1023​.html
    def test_apple_rle_example(self):
        """Example from Apple TN1023, where the packed data is shorter than the unpacked data."""
        unpacked = array(
            "B",
            [
                0xAA,
                0xAA,
                0xAA,
                0x80,
                0x00,
                0x2A,
                0xAA,
                0xAA,
                0xAA,
                0xAA,
                0x80,
                0x00,
                0x2A,
                0x22,
                0xAA,
                0xAA,
                0xAA,
                0xAA,
                0xAA,
                0xAA,
                0xAA,
                0xAA,
                0xAA,
                0xAA,
            ],
        )
        packed = run_length_encode(unpacked)
        expected = array(
            "B",
            [
                0xFE,
                0xAA,
                0x02,
                0x80,
                0x00,
                0x2A,
                0xFD,
                0xAA,
                0x03,
                0x80,
                0x00,
                0x2A,
                0x22,
                0xF7,
                0xAA,
            ],
        )
        self.assertEqual(expected, packed)

    def test_longer_rle(self):
        """Example where the packed data is longer than the unpacked data."""
        unpacked = array("B", [0x55, 0x55, 0xBB, 0xBB, 0x55, 0xBB, 0xBB, 0x55])
        packed = run_length_encode(unpacked)
        expected = array(
            "B", [0xFF, 0x55, 0xFF, 0xBB, 0x00, 0x55, 0xFF, 0xBB, 0x00, 0x55]
        )
        self.assertEqual(expected, packed)

    def test_simple_literal(self):
        """Example where there is a simple literal run of 5 bytes."""
        unpacked = array("B", [0x00, 0x01, 0x02, 0x03, 0x04])
        packed = run_length_encode(unpacked)
        expected = array("B", [0x04, 0x00, 0x01, 0x02, 0x03, 0x04])
        self.assertEqual(expected, packed)

    def test_simple_literal2(self):
        """Example where there is a simple literal of 1 byte to pack."""
        unpacked = array("B", [0x00])
        packed = run_length_encode(unpacked)
        expected = array("B", [0x00, 0x00])
        self.assertEqual(expected, packed)

    def test_simple_same(self):
        """Example where there is a simple run of 4 same bytes to pack."""
        unpacked = array("B", [0x11, 0x11, 0x11, 0x11])
        packed = run_length_encode(unpacked)
        expected = array("B", [0xFD, 0x11])
        self.assertEqual(expected, packed)

    def test_simple_same2(self):
        """Example where there are two simple runs of 4 same bytes to pack."""
        unpacked = array("B", [0x11, 0x11, 0x11, 0x11, 0x22, 0x22, 0x22, 0x22])
        packed = run_length_encode(unpacked)
        expected = array("B", [0xFD, 0x11, 0xFD, 0x22])
        self.assertEqual(expected, packed)


if __name__ == "__main__":
    unittest.main()
