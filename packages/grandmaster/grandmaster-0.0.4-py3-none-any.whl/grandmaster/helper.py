from typing import Union
from io import BytesIO
from PIL import Image
from fastapi import UploadFile
import requests


def read_image(image: Union[str, bytes, BytesIO, Image.Image]) -> UploadFile:
    """
    Reads an image from a file path, bytes, BytesIO, PIL Image object, or URL,
    and returns a FastAPI UploadFile object.
    """
    if isinstance(image, str):
        if image.startswith("http"):
            response = requests.get(image)
            contents = response.content
        else:
            with open(image, "rb") as f:
                contents = f.read()
    elif isinstance(image, bytes):
        contents = image
    elif isinstance(image, BytesIO):
        contents = image.getvalue()
    elif isinstance(image, Image.Image):
        with BytesIO() as output:
            image.save(output, format="PNG")
            contents = output.getvalue()
    else:
        raise TypeError(
            "Invalid input image type. Must be str, bytes, BytesIO, PIL Image, or URL."
        )

    binary_io = BytesIO(contents)
    return UploadFile(filename="image.png", file=binary_io)
