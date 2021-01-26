import os
from binascii import hexlify
from typing import Optional

from PIL import Image, ImageDraw, ImageFont
from pydantic import BaseModel

from string_avatar import utils

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseAvatar(BaseModel):
    string: str
    size: int = 250
    bgcolor: str = "black"
    font_path: str = os.path.join(basedir, "fonts", "GentiumPlus-R.ttf")
    font_color: str = "white"
    font_outline_width: int = 0
    font_outline_color: Optional[str] = None

    def generate(self) -> Image:
        img = self.get_empty_image()
        img = self.draw_letter(img)
        return img

    def draw_letter(self, img: Image) -> Image:
        font = ImageFont.truetype(self.font_path, size=self.size)
        draw = ImageDraw.Draw(img)
        letter = self.string[0].upper()
        text_width, text_height = draw.textsize(letter, font)
        offset_x, offset_y = font.getoffset(letter)
        position = (
            (self.size / 2 - (text_width + offset_x) / 2),
            (self.size / 2 - (text_height + offset_y) / 2),
        )
        draw.text(
            position,
            letter,
            font=font,
            fill=self.font_color,
            stroke_fill=self.font_outline_color,
            stroke_width=self.font_outline_width,
        )
        return img

    def get_empty_image(self) -> Image:
        img = Image.new(mode="RGB", size=(self.size, self.size), color=self.bgcolor)
        return img


class CharAvatar(BaseAvatar):
    def __init__(self, string: str, **kwargs):
        value = utils.get_string_value(string)

        light_bytes = utils.get_rgb_from_value(value)
        light_color = "#" + hexlify(bytearray(light_bytes)).decode("ascii")

        dark_bytes = [v // 2 for v in light_bytes]
        dark_color = "#" + hexlify(bytearray(dark_bytes)).decode("ascii")

        d = {
            "string": string,
            "bgcolor": dark_color,
            "font_color": light_color,
            "font_outline_color": "white",
            "font_outline_width": 2,
        }

        d.update(kwargs)
        print(d)

        super().__init__(**d)


if __name__ == "__main__":
    import sys

    s = sys.argv[1]
    CharAvatar(string=s).generate().show()
