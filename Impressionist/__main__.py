from argparse import ArgumentParser

from Impressionist.impressionist import ColorMethod, Impressionist, ShapeType

if __name__ == "__main__":
    # Parse the file arguments.
    argument_parser = ArgumentParser("Impressionist")
    argument_parser.add_argument("image_file", help="The input image.")
    argument_parser.add_argument("output_file", help="The resulting abstract art.")
    argument_parser.add_argument(
        "-t",
        "--trials",
        type=int,
        default=10_000,
        help="The number of trials to run (default 10,000).",
    )
    argument_parser.add_argument(
        "-m",
        "--method",
        choices=["random", "average", "common"],
        default="average",
        help="Shape color determination method (default average).",
    )
    argument_parser.add_argument(
        "-s",
        "--shape",
        choices=["ellipse", "triangle", "quadrilateral", "line"],
        default="ellipse",
        help="The shape type (default ellipse).",
    )
    argument_parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=256,
        help="The length of the final image in pixels (default 256).",
    )
    argument_parser.add_argument(
        "-v",
        "--vector",
        default=False,
        action="store_true",
        help="Create vector output. A SVG file will also be output.",
    )
    argument_parser.add_argument(
        "-a",
        "--animate",
        type=int,
        default=0,
        help=(
            "If greater than 0, it will create an animated GIF with the number"
            " of milliseconds per frame provided. WARNING: High resolutions + "
            "animations may consume significant memory."
        ),
    )
    arguments = argument_parser.parse_args()
    method = ColorMethod[arguments.method.upper()]
    shape_type = ShapeType[arguments.shape.upper()]
    Impressionist(
        arguments.image_file,
        arguments.output_file,
        arguments.trials,
        method,
        shape_type,
        arguments.length,
        arguments.vector,
        arguments.animate,
    )
