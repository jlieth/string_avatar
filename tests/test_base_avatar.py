import pytest
from PIL import ImageColor
from pydantic.error_wrappers import ValidationError

from string_avatar.avatars import BaseAvatar


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

        # test passing values
        avatar = BaseAvatar(
            string="test",
            size=600,
            bgcolor="#fff",
            font_path="test.ttf",
            font_color="black",
        )
        assert avatar.size == 600
        assert avatar.bgcolor == "#fff"
        assert avatar.font_path.endswith("test.ttf")
        assert avatar.font_color == "black"

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
