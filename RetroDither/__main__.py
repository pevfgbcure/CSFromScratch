from PIL import Image
from RetroDither.macpaint import MAX_HEIGHT, MAX_WIDTH


def prepare(file_name: str) -> Image.Image:
    """Prepares the image for dithering by resizing it to fit within the maximum
    dimensions of the original MacPaint and converting it to grayscale.

    Args:
        file_name: The path to the image file to prepare.

    Returns:
        The prepared image.
    """
    with open(file_name, "rb") as fp:
        image = Image.open(fp)
        # Resize the image to fit the maximum of the original MacPaint.
        if image.width > MAX_WIDTH or image.height > MAX_HEIGHT:
            desired_ratio = MAX_WIDTH / MAX_HEIGHT
            ratio = image.width / image.height
            if ratio >= desired_ratio:
                new_size = (MAX_WIDTH, int(image.height * (MAX_WIDTH / image.width)))
            else:
                new_size = (int(image.width * (MAX_HEIGHT / image.height)), MAX_HEIGHT)
            image.thumbnail(new_size, Image.Resampling.LANCZOS)
        # Convert to grayscale
        return image.convert("L")
