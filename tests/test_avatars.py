import pytest
from PIL import ImageColor
from pydantic.error_wrappers import ValidationError

from string_avatar.avatars import BaseAvatar, CharAvatar


class TestBaseAvatar:
    def test_params(self):
        # creating an avatar without string parameter should raise error
        with pytest.raises(ValidationError):
            BaseAvatar()

        # test default values
        avatar = BaseAvatar(string="test")
        assert avatar.size == 250
        assert avatar.bgcolor == "black"
        assert avatar.font_path.endswith("GentiumPlus-R.ttf")
        assert avatar.font_color == "white"
        assert avatar.font_outline_width == 0
        assert avatar.font_outline_color is None

        # test passing values
        avatar = BaseAvatar(
            string="test",
            size=600,
            bgcolor="#fff",
            font_path="test.ttf",
            font_color="black",
            font_outline_width=5,
            font_outline_color="blue",
        )
        assert avatar.size == 600
        assert avatar.bgcolor == "#fff"
        assert avatar.font_path.endswith("test.ttf")
        assert avatar.font_color == "black"
        assert avatar.font_outline_width == 5
        assert avatar.font_outline_color == "blue"

    def test_draw_letter(self):
        """Tests that a letter is drawn on the image"""

        # for the letter T, center of the image should be lime
        avatar = BaseAvatar(string="t", font_color="lime")
        img = avatar.get_empty_image()
        img = avatar.draw_letter(img)
        center = (avatar.size / 2, avatar.size / 2)
        expected_color = ImageColor.getrgb(avatar.font_color)
        actual_color = img.getpixel(center)
        assert actual_color == expected_color

        # for the letter O, center of the image should be bgcolor
        avatar = BaseAvatar(string="o", font_color="lime")
        img = avatar.get_empty_image()
        img = avatar.draw_letter(img)
        center = (avatar.size / 2, avatar.size / 2)
        expected_color = ImageColor.getrgb(avatar.bgcolor)
        actual_color = img.getpixel(center)
        assert actual_color == expected_color

    def test_get_empty_image(self):
        avatar = BaseAvatar(string="test", size=10, bgcolor="lightblue")
        img = avatar.get_empty_image()

        # test width and height
        assert img.height == avatar.size
        assert img.width == avatar.size

        # test mode
        assert img.mode == "RGB"

        # test bgcolor
        bgcolor = ImageColor.getrgb(avatar.bgcolor)
        img_color = img.getpixel((0, 0))
        assert img_color == bgcolor


class TestCharAvatar:
    def test_generated_values(self):
        """Tests calculated colors against known values"""
        avatar = CharAvatar(string="test")

        assert avatar.bgcolor == "#77007f"
        assert avatar.font_color == "#ee00ff"
        assert avatar.font_outline_color == "white"
        assert avatar.font_outline_width == 2

    def test_overriding_values(self):
        """Tests that passing kwargs overrides calculated values"""
        avatar = CharAvatar(
            string="test",
            size=500,
            bgcolor="black",
            font_color="magenta",
            font_outline_color="#fff",
            font_outline_width=5,
        )

        assert avatar.size == 500
        assert avatar.bgcolor == "black"
        assert avatar.font_color == "magenta"
        assert avatar.font_outline_color == "#fff"
        assert avatar.font_outline_width == 5
