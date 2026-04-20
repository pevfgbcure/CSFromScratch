from enum import Enum
from PIL import Image, ImageDraw
from PIL import ImageChops, ImageStat
import random
from math import trunc
from timeit import default_timer as timer
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