import os
import random
from io import BytesIO
from urllib.parse import urlparse

import requests
from PIL import Image, ImageDraw, ImageFont


class MemeEngine:
    """Base class that is able to generate meme images based on user
    inputs like image path (URL or path), quote body and author.
    """

    _font_path = "./fonts/LilitaOne-Regular.ttf"

    def __init__(self, dir_path):
        """Create a new MemeEngine, saving to given directory.

        Args:
            dir_path (_type_): which directory to save into.
        """
        os.makedirs(dir_path, exist_ok=True)  # silently fail if exists
        self.dir_path = dir_path

    def make_meme(self, img_path, text, author, width=500):
        """Make a meme from a given image, text and author with default
        width of 500 pixels.

        Args:
            img_path (_type_): path to image
            text (_type_): body of meme text
            author (_type_): author of meme text
            width (int, optional): Desired final width of meme, defaults
              to a max of 500.
        """
        safe_width = width if width <= 500 else 500

        img = self._get_resized_image(img_path, safe_width)
        self._draw_text(img, text, author, safe_width)
        filepath = f"{self.dir_path}/{random.randint(0, 10000000)}.png"

        with open(filepath, "wb") as out_file:
            img.save(out_file)

        return filepath

    def _get_resized_image(self, img_path, width):
        """Given a file path or URL, return a resized image resized
        proportionally to a given width. Note, the resize calc can
        up or downscale: height = int(vert_size * width / hor_size)

        Args:
            img_path (str): path or url to the image file
            width (int): Resize image proportionally to this width.

        Returns:
            PIL.Image: a resized PIL.Image
        """
        try:
            if self._is_url(img_path):
                response = requests.get(img_path, timeout=10)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
            else:
                img = Image.open(img_path)
            hor_size, vert_size = img.size
            height = int(vert_size * width / hor_size)
            resized = img.resize(
                (width, height),
                Image.Resampling.NEAREST,
            )
            return resized
        except FileNotFoundError as e:
            print(f"Could not find file. {e}")
            raise
        except Exception as e:
            print(f"Could not resize image: {e}")
            raise

    def _is_url(self, path: str) -> bool:
        """Checks if a path str from the user is a URL so we may use
        the appropriate method of fetching the image to make a meme
        out of.

        Args:
            path (str): A path or URL string

        Returns:
            bool: whether the path is actually an URL
        """
        parsed = urlparse(path)
        return parsed.scheme in ("http", "https")

    def _draw_text(self, img, text, author, width):
        """Draw the meme text onto the given image.

        Args:
            img (_type_): The image
            text (_type_): The quote body text
            author (_type_): The quote's author
            width (_type_): Used to line up both text fields
        """
        try:
            font_size = int(width / 20)

            text_position = self._get_rand_x_y(img.size[0], img.size[1])
            author_position = self._get_rand_x_y(img.size[0], img.size[1])

            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(self._font_path, size=font_size)

            draw.text(text_position, text, font=font, fill="white")
            draw.text(author_position, author, font=font, fill="white")
        except Exception as e:
            print(f"Could not draw text on meme: {e}")
            raise

    def _get_rand_x_y(self, width, length):
        """Returns a random tuple of (x,y) but does attempt to keep text
        on the left of the image

        Args:
            width (int): Width of image
            length (int): Length of image

        Returns:
            tuple: Tuple of (x,y)
        """
        x = random.randint(0, int(width / 2))
        y = random.randint(0, int(length / 2))
        return (x, y)
