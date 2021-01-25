import pytest

from string_avatar import utils


def test_get_string_value():
    # test a couple of known values to ensure reproducibility
    known_values = [
        ("a", 0.9517993074362573),
        ("ü", 0.6067902434116036),
        ("foobar", 0.9388876586194379),
    ]

    for s, expected in known_values:
        value = utils.get_string_value(s)
        assert value == pytest.approx(expected)


def test_get_rgb_from_value():
    known_values = [
        (0, (255, 0, 0)),
        (0.166667, (255, 255, 0)),
        (0.333333, (0, 255, 0)),
        (0.5, (0, 255, 255)),
        (0.666667, (0, 0, 255)),
        (0.833333, (255, 0, 255)),
        (1, (255, 0, 0)),
    ]

    for v, expected in known_values:
        color = utils.get_rgb_from_value(v)
        assert color == expected


class TestColorFromString:
    """Tests string_avatar.utils.get_colors_from_string"""

    def test_single_char(self):
        s = "a"
        colors = utils.get_colors_from_string(s)
        assert len(colors) == 1
        assert colors[0] == (255, 0, 74)

    def test_unique_parameter(self):
        s = "aa"

        # two identical characters should return one color for unique=True
        colors = utils.get_colors_from_string(s, unique=True)
        assert len(colors) == 1
        assert colors[0] == (255, 0, 74)

        # identical chars should return two identical colors for unique=False
        colors = utils.get_colors_from_string(s, unique=False)
        assert len(colors) == 2
        assert colors[0] == colors[1] == (255, 0, 74)

    def test_full_ascii(self):
        s = "".join(chr(i) for i in range(128))

        colors = utils.get_colors_from_string(s)
        assert len(colors) == len(s)


class TestGeometricTransformation:
    """Tests string_avatar.utils.GeometricTransformation"""

    def test_axes_start_at_zero(self):
        """Tests transform with axes that start at zero"""
        in_x_axis = (0, 10)
        in_y_axis = (0, 5)
        out_x_axis = (0, 5)
        out_y_axis = (0, 10)

        transform = utils.GeometricTransformation(
            in_x_axis, in_y_axis, out_x_axis, out_y_axis
        )

        point = (2, 3)
        point_transformed = transform.get(point)
        assert point_transformed == (1, 6)

    def test_axes_with_offset(self):
        """Tests transform with axes that have an offset (min != 0)"""
        in_x_axis = (-1, 6)
        in_y_axis = (4, 9)
        out_x_axis = (2, 16)
        out_y_axis = (-5, 5)

        transform = utils.GeometricTransformation(
            in_x_axis, in_y_axis, out_x_axis, out_y_axis
        )

        point = (2, 5)
        point_transformed = transform.get(point)

        assert point_transformed == (8, -3)

    def test_reverse_axes(self):
        """Tests transform with axes that are given in reverse (max, min)"""
        in_x_axis = (5, 12)
        in_y_axis = (4, 9)
        out_x_axis = (10, 3)
        out_y_axis = (8, 3)

        transform = utils.GeometricTransformation(
            in_x_axis, in_y_axis, out_x_axis, out_y_axis
        )

        point = (7, 8)
        point_transformed = transform.get(point)

        assert point_transformed == (8, 4)
