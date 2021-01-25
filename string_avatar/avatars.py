import os

from PIL import Image, ImageDraw, ImageFont
from pydantic import BaseModel

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseAvatar(BaseModel):
    string: str
    size: int = 250
    bgcolor: str = "black"
    font_path: str = os.path.join(basedir, "fonts", "GentiumPlus-R.ttf")
    font_color: str = "white"

    def generate(self) -> Image:
        img = self.get_empty_image()
        img = self.draw_letter(img)
        return img

    def draw_letter(self, img: Image) -> Image:
        font = ImageFont.truetype(self.font_path, size=int(0.9 * self.size))
        draw = ImageDraw.Draw(img)
        letter = self.string[0].upper()
        text_width, text_height = draw.textsize(letter, font)
        offset_x, offset_y = font.getoffset(letter)
        position = (
            (self.size / 2 - (text_width + offset_x) / 2),
            (self.size / 2 - (text_height + offset_y) / 2),
        )
        draw.text(position, letter, font=font, fill=self.font_color)
        return img

    def get_empty_image(self) -> Image:
        img = Image.new(mode="RGB", size=(self.size, self.size), color=self.bgcolor)
        return img


if __name__ == "__main__":
    import sys

    s = sys.argv[1]
    BaseAvatar(string=s, font_color="lime", bgcolor="black").generate().show()
