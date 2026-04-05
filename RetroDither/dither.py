from array import array
from typing import NamedTuple

from PIL import Image

THRESHOLD = 127


class PatternPart(NamedTuple):
    dc: int  # Change in column.
    dr: int  # change in row.
    numerator: int
    denominator: int


ATKINSON = [
    PatternPart(1, 0, 1, 8),
    PatternPart(2, 0, 1, 8),
    PatternPart(-1, 1, 1, 8),
    PatternPart(0, 1, 1, 8),
    PatternPart(1, 1, 1, 8),
    PatternPart(0, 2, 1, 8),
]


def dither(image: Image.Image) -> array:
    """Applies the Atkinson dithering algorithm to the given image.

    Args:
        image: The image to dither. Must be in grayscale (mode "L" in Pillow).

    Returns:
        An array of dithered pixel values (255 for white, 0 for black).
    """

    # Distribute error among nearby pixels
    def diffuse(c: int, r: int, error: int, pattern: list[PatternPart]):
        for part in pattern:
            col = c + part.dc
            row = r + part.dr
            if col < 0 or col >= image.width or row >= image.height:
                continue
            current_pixel: float = image.getpixel((col, row))
            # Add error_part to the pixel at (col, row) in image.
            error_part = (error * part.numerator) // part.denominator
            image.putpixel((col, row), current_pixel + error_part)

    result = array("B", [0] * (image.width * image.height))
    for y in range(image.height):
        for x in range(image.width):
            old_pixel: float = image.getpixel((x, y))
            # Every new pixel is either solid white or solid black
            #  since this is what the original Macintosh supported.
            new_pixel = 255 if old_pixel > THRESHOLD else 0
            result[y * image.width + x] = new_pixel
            difference = int(old_pixel - new_pixel)
            # Disperse error among nearby upcoming pixels.
            diffuse(x, y, difference, ATKINSON)

    return result
