import random
from enum import Enum
from math import trunc
from timeit import default_timer as timer

from PIL import Image, ImageChops, ImageDraw, ImageStat  # noqa: F401

from Impressionist.svg import SVG  # noqa: F401

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
        self.shapes: list[tuple[CoordList, tuple[int, int, int]]] = []
        # Open the image file and store it in instance variable, then execute algorithm.
        with open(file_name, "rb") as fp:
            self.original = Image.open(fp).convert("RGB")
            # Scale down image so processing is faster, 256 max height pixel dimension.
            width, height = self.original.size
            aspect_ratio = width / height
            new_size = (int(MAX_HEIGHT * aspect_ratio), MAX_HEIGHT)
            self.original.thumbnail(new_size, Image.Resampling.LANCZOS)
            # Start the generated image with a background that is the average of all of
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
            print("ALL DONE.")

    def difference(self, other_image: Image.Image) -> float:
        """Returns a ratio of how different the other image is from the original image.
        0 means the same, 1 means completely different.

        Args:
            other_image: The image to compare to the original.

        Returns:
            A float between 0 and 1 representing how different the other image is
                from the original.
        """

        diff = ImageChops.difference(self.original, other_image)
        stat = ImageStat.Stat(diff)
        diff_ratio = sum(stat.mean) / (len(stat.mean) * 255)
        return diff_ratio

    def random_coordinates(self) -> CoordList:
        """Generates a list of random coordinates for the shape to be drawn at.
        The number of coordinates depends on the shape type.

        Returns:
            A list of random coordinates for the shape to be drawn at.
        """

        num_coordinates = 4  # For an ellipse or a line.
        if self.shape_type == ShapeType.TRIANGLE:
            num_coordinates = 6
        elif self.shape_type == ShapeType.QUADRILATERAL:
            num_coordinates = 8
        coordinates = []
        for d in range(num_coordinates):
            if d % 2 == 0:  # x-coordinates.
                coordinates.append(random.randint(0, self.original.width))
            else:  # y-coordinates.
                coordinates.append(random.randint(0, self.original.height))
        return coordinates

    @staticmethod
    def bounding_box(coordinates: CoordList) -> tuple[int, int, int, int]:
        """Returns the bounding box of the shape defined by the coordinates.

        Args:
            coordinates: A list of coordinates defining the shape.

        Returns:
            A tuple of four integers representing the bounding box (x1, y1, x2, y2).
        """

        xcoords = coordinates[::2]
        ycoords = coordinates[1::2]
        x1 = min(xcoords)
        y1 = min(ycoords)
        x2 = max(xcoords)
        y2 = max(ycoords)
        return x1, y1, x2, y2

    def trial(self):
        """Performs a single trial of the algorithm, which involves generating a random
        shape, determining its color, and checking if it improves the similarity to the
        original image.
        """

        while True:
            coordinates = self.random_coordinates()
            region = self.original.crop(self.bounding_box(coordinates))
            if region.width > 0 and region.height > 0:
                break

        if self.method == ColorMethod.AVERAGE:
            color = tuple((round(n) for n in ImageStat.Stat(region).mean))
        elif self.method == ColorMethod.COMMON:
            color = get_most_common_color(region)
        else:  # Must be a random color.
            color = tuple(random.choices(range(256), k=3))
        original = self.glass

        def experiment() -> bool:
            """Draw the shape on a copy of the current image, and check if it improves the
            similarity to the original image. If it does, update the current image and
            best difference.

            Returns:
                True if the shape improves the similarity, False otherwise.
            """

            new_image = original.copy()
            glass_draw = ImageDraw.Draw(new_image)
            if self.shape_type == ShapeType.ELLIPSE:
                glass_draw.ellipse(self.bounding_box(coordinates), fill=color)
            else:  # Must be a triangle, quadrilateral or line.
                glass_draw.polygon(coordinates, fill=color)

            new_difference = self.difference(new_image)
            if new_difference < self.best_difference:
                self.best_difference = new_difference
                self.glass = new_image
                return True
            return False

        if experiment():
            # Try expanding on every direction, and keep going in better directions.
            for index in range(len(coordinates)):
                for amount in (-1, 1):
                    while True:
                        old_coordinates = coordinates.copy()
                        coordinates[index] = coordinates[index] + amount
                        if not experiment():
                            coordinates = old_coordinates
                            break
            self.shapes.append((coordinates, color))

    def create_output(
        self, out_file: str, height: int, vector: bool, animation_length: int
    ):
        """Creates the output image (and SVG if vector is True) by drawing all the shapes
        on a blank canvas with the average color as the background.

        Args:
            out_file: The path to the output image file.
            height: The height of the final image in pixels.
            vector: Whether to create vector output (SVG).
            animation_length: If greater than 0, creates an animated GIF with the number of
                milliseconds per frame provided.
        """

        average_color = tuple((round(n) for n in ImageStat.Stat(self.original).mean))
        original_width, original_height = self.original.size
        ratio = height / original_height
        output_size = (int(original_width * ratio), int(original_height * ratio))
        output_image = Image.new("RGB", output_size, average_color)
        output_draw = ImageDraw.Draw(output_image)
        svg = SVG(*output_size, background_color=average_color) if vector else None
        animation_frames: list[Image.Image] | None = (
            [] if animation_length > 0 else None
        )

        # Calculate frame sampling to avoid excessive memory use.
        frame_sample_rate = 1
        if animation_frames is not None and len(self.shapes) > 100:
            # Limit to ~100 frames maximum to prevent memory exhaustion.
            frame_sample_rate = max(1, len(self.shapes) // 100)
            print(
                f"Sampling every {frame_sample_rate} frame(s) for animation to manage memory."
            )

        for shape_index, (coordinate_list, color) in enumerate(self.shapes):
            # Scale each coordinate to the correct size.
            coordinates = [int(x * ratio) for x in coordinate_list]
            if self.shape_type == ShapeType.ELLIPSE:
                output_draw.ellipse(self.bounding_box(coordinates), fill=color)
                if svg:
                    svg.draw_ellipse(*coordinates, color=color)
            else:  # The shape must be a triangle, quadrilateral or line.
                output_draw.polygon(coordinates, fill=color)
                if svg:
                    if self.shape_type == ShapeType.LINE:
                        svg.draw_line(*coordinates, color=color)
                    else:
                        svg.draw_polygon(coordinates, color)
            if animation_frames is not None and shape_index % frame_sample_rate == 0:
                animation_frames.append(output_image.copy())

        output_image.save(out_file)
        if svg:
            svg.write(out_file + ".svg")
        if animation_frames is not None and len(animation_frames) > 0:
            print(f"Creating animated GIF with {len(animation_frames)} frames.")
            animation_frames[0].save(
                out_file + ".gif",
                format="GIF",
                save_all=True,
                append_images=animation_frames[1:] if len(animation_frames) > 1 else [],
                optimize=False,
                duration=animation_length,
                loop=0,
                transparency=0,
                disposal=2,
            )
