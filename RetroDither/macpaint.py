from array import array

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
