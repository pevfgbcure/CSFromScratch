class SVG:
    """A simple class to create SVG files."""

    def __init__(self, width: int, height: int, background_color: tuple[int, int, int]):
        """Initialize the SVG content with the header and background.

        Args:
            width: The width of the SVG canvas.
            height: The height of the SVG canvas.
            background_color: The background color as an RGB tuple (e.g., (255, 255, 255) for white).
        """

        self.content = (
            '<?xml version="1.0" encoding="utf-8"?>\n'
            f'<svg version="1.1" baseProfile="full" width="{width}" '
            f'height="{height}" xmlns="http://www.w3.org/2000/svg">\n'
            f'<rect width="100%" height="100%" fill="rgb{background_color}" />'
        )

    def draw_ellipse(
        self, x1: int, y1: int, x2: int, y2: int, color: tuple[int, int, int]
    ):
        """Draw an ellipse defined by the bounding box (x1, y1) to (x2, y2) with the specified color.

        Args:
            x1: The x-coordinate of the top-left corner of the bounding box.
            y1: The y-coordinate of the top-left corner of the bounding box.
            x2: The x-coordinate of the bottom-right corner of the bounding box.
            y2: The y-coordinate of the bottom-right corner of the bounding box.
            color: The fill color as an RGB tuple (e.g., (255, 0, 0) for red).
        """

        self.content += (
            f'<ellipse cx="{(x1 + x2) // 2}" cy="{(y1 + y2) // 2}" '
            f'rx="{abs(x1 - x2) // 2}" ry="{abs(y1 - y2) // 2}" '
            f'fill="rgb{color}" />\n'
        )

    def draw_line(
        self, x1: int, y1: int, x2: int, y2: int, color: tuple[int, int, int]
    ):
        """Draw a line from (x1, y1) to (x2, y2) with the specified color.

        Args:
            x1: The x-coordinate of the starting point.
            y1: The y-coordinate of the starting point.
            x2: The x-coordinate of the ending point.
            y2: The y-coordinate of the ending point.
            color: The stroke color as an RGB tuple (e.g., (255, 0, 0) for red).
        """

        self.content += (
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="rgb{color}" '
            'stroke-width="1px" shape-rendering="crispEdges" />\n'
        )

    def draw_polygon(self, coordinates: list[int], color: tuple[int, int, int]):
        """Draw a polygon defined by the list of coordinates with the specified color.

        Args:
            coordinates: A list of integers representing the vertices of the polygon in the format [x1, y1, x2, y2, ...].
            color: The fill color as an RGB tuple (e.g., (255, 0, 0) for red).
        """

        points = ""
        for index in range(0, len(coordinates), 2):
            points += f"{coordinates[index]},{coordinates[index + 1]} "
        self.content += f'<polygon points="{points}" fill="rgb{color}" />\n'

    def write(self, path: str):
        """Finalize the SVG content and write it to the specified file path.

        Args:
            path: The file path where the SVG content will be written.
        """

        self.content += "</svg>\n"
        with open(path, "w") as file:
            file.write(self.content)
