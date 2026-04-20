import random
from enum import Enum
from math import trunc
from timeit import default_timer as timer

from PIL import Image, ImageChops, ImageDraw, ImageStat

from Impressionist.svg import SVG

ColorMethod = Enum("ColorMethod", "RANDOM AVERAGE COMMON")
ShapeType = Enum("ShapeType", "ELLIPSE TRIANGLE QUADRILATERAL LINE")
CoordList = list[int]
MAX_HEIGHT = 256


def get_most_common_color(image: Image.Image) -> tuple[int, int, int]:
    """Returns the most common color in the image.

    Args:
        image: The image to analyze.

    Returns:
        The most common color in the image as an (R, G, B) tuple.
    """

    colors = image.getcolors(image.width * image.height)
    return max(colors, key=lambda item: item[0])[1]


class Impressionist:
    """Impressionist is a class that takes an image and creates an abstract art version
    of it using a specified shape type and color method. The algorithm works by randomly
    generating shapes and comparing the resulting image to the original, keeping the shape
    if it improves the similarity."""

    def __init__(
        self,
        file_name: str,
        output_file: str,
        trials: int,
        method: ColorMethod,
        shape_type: ShapeType,
        length: int,
        vector: bool,
        animation_length: int,
    ):
        """Initializes the Impressionist class and runs the algorithm.

        Args:
            file_name: The path to the input image file.
            output_file: The path to the output image file.
            trials: The number of trials to run.
            method: The method to determine the color of the shapes.
            shape_type: The type of shape to use in the abstract art.
            length: The length of the final image in pixels.
            vector: Whether to create vector output (SVG).
            animation_length: If greater than 0, creates an animated GIF with the number of
                milliseconds per frame provided.
        """

        self.method = method
        self.shape_type = shape_type
        self.shapes = []
        # Open the image file and store it in instance variable, then execute algorithm.
        with open(file_name, "rb") as fp:
            self.original = Image.open(fp).convert("RGB")
            # Scale down image so processing is faster, 256 max height pixel dimension.
            width, height = self.original.size
            aspect_ratio = width / height
            new_size = (int(MAX_HEIGHT * aspect_ratio), MAX_HEIGHT)
            self.original.thumbnail(new_size, Image.Resampling.LANCZOS)
            # Start the generated image with a background that is the average of all
            # the original's pixels in color.
            average_color = tuple(round(n) for n in ImageStat.Stat(self.original).mean)
            self.glass = Image.new("RGB", new_size, average_color)
            # Keep track of how far along we are, our best result so far, and how much
            # time elapses as the processing takes place.
            self.best_difference = self.difference(self.glass)
            last_percent = 0
            start = timer()
            for test in range(trials):
                self.trial()
                percent = trunc(test / trials * 100)
                if percent > last_percent:
                    last_percent = percent
                    print(f"{percent}% Done, Best difference {self.best_difference}")
            end = timer()
            print(f"{end - start} seconds elapsed. {len(self.shapes)} shapes created.")
            self.create_output(output_file, length, vector, animation_length)
