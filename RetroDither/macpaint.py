from array import array
from datetime import datetime
from pathlib import Path

MAX_WIDTH = 576
MAX_HEIGHT = 720
MACBINARY_LENGTH = 128
HEADER_LENGTH = 512


def bytes_to_bits(original: array) -> array:
    """Converts an array of bytes where each byte is 0 or 255 to an array of bits
    where each byte that is 0 becomes a 1 and each byte that is 255 becomes a 0.

    Args:
        original: An array of bytes where each byte is either 0 or 255.

    Returns:
        An array of bytes where each byte is either 0 or 1, representing the bits.
    """
    bits_array = array("B")

    for byte_index in range(0, len(original), 8):
        next_byte = 0
        for bit_index in range(8):
            next_bit = 1 - (original[byte_index + bit_index] & 1)
            next_byte = next_byte | (next_bit << (7 - bit_index))
            if (byte_index + bit_index + 1) >= len(original):
                break

        bits_array.append(next_byte)
    return bits_array


def prepare(data: array, width: int, height: int) -> array:
    """Convert the array of bytes into bits using the bytes_to_bits function. Pad
    any missing spots with white pixels (0 in bits) due to the original dithered
    image being smaller than the maximum supported size of 576x720.

    Args:
        data: An array of bytes where each byte is either 0 or 255, representing
            the dithered image.
        width: The width of the original dithered image.
        height: The height of the original dithered image.

    Returns:
        An array of bytes where each byte is either 0 or 1, representing the bits
            of the image, padded to the maximum supported size.
    """
    bits_array = array("B")
    for row in range(height):
        image_location = row * width
        image_bits = bytes_to_bits(data[image_location : (image_location + width)])
        bits_array += image_bits
        remaining_width = MAX_WIDTH - width
        white_width_bits = array("B", [0] * (remaining_width // 8))
        bits_array += white_width_bits

    remaining_height = MAX_HEIGHT - height
    white_height_bits = array("B", [0] * ((remaining_height * MAX_WIDTH) // 8))
    bits_array += white_height_bits
    return bits_array


def run_length_encode(original_data: array) -> array:
    """Encodes the original data using run-length encoding.

    - 0 to 127 (inclusive) means that the next (n + 1) bytes are not the same and should be copied as is.
    - 129 to 255 (inclusive) means that the next byte should be repeated (257 - n) times.
    - 128 is not used and should be ignored if it appears.

    Args:
        original_data: An array of bytes to encode.

    Returns:
        An array of bytes representing the run-length encoded data.
    """

    # Find how many of the same bytes are in a row from the 'start' position.
    def take_same(source: array, start: int) -> int:
        count = 0
        while (
            start + count + 1 < len(source)
            and source[start + count] == source[start + count + 1]
        ):
            count += 1
        return count + 1 if count > 0 else 0

    rle_data = array("B")
    # Divide data into MAX_WIDTH size boundaries by line.
    for row_start in range(0, len(original_data), MAX_WIDTH // 8):
        row_data = original_data[row_start : (row_start + (MAX_WIDTH // 8))]
        byte_index = 0
        while byte_index < len(row_data):
            not_same_bytes = 0
            while (
                (same_bytes := take_same(row_data, byte_index + not_same_bytes)) == 0
            ) and (byte_index + not_same_bytes < len(row_data)):
                not_same_bytes += 1
            if not_same_bytes > 0:
                rle_data.append(not_same_bytes - 1)
                rle_data += row_data[byte_index : byte_index + not_same_bytes]
                byte_index += not_same_bytes
            if same_bytes > 0:
                rle_data.append(257 - same_bytes)
                rle_data.append(row_data[byte_index])
                byte_index += same_bytes
    return rle_data


def macbinary_header(outfile: str, data_size: int) -> array:
    """Creates a MacBinary header for the given output file name and data size.

    Args:
        outfile: The name of the output file.
        data_size: The size of the data fork in bytes.

    Returns:
        An array of bytes representing the MacBinary header.
    """
    macbinary = array("B", [0] * MACBINARY_LENGTH)
    filename = Path(outfile).stem
    filename = (
        filename[:63] if len(filename) > 63 else filename
    )  # Limit to 63 chars max.
    macbinary[1] = len(filename)  # Filename length.
    macbinary[2 : (2 + len(filename))] = array(
        "B", filename.encode("mac_roman")
    )  # Filename.
    macbinary[65:69] = array("B", "PNTG".encode("mac_roman"))  # File type.
    macbinary[69:73] = array("B", "MPNT".encode("mac_roman"))  # File creator.
    macbinary[83:87] = array(
        "B", data_size.to_bytes(4, byteorder="big")
    )  # Size of data fork.
    timestamp = int(
        (datetime.now() - datetime(1904, 1, 1)).total_seconds()
    )  # Mac timestamp.
    macbinary[91:95] = array(
        "B", timestamp.to_bytes(4, byteorder="big")
    )  # Creation stamp.
    macbinary[95:99] = array(
        "B", timestamp.to_bytes(4, byteorder="big")
    )  # Modification stamp.
    return macbinary
