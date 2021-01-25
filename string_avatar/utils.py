import colorsys
import hashlib
import random
from typing import List, Tuple


def get_colors_from_string(s: str, unique: bool = True) -> List[Tuple[int, int, int]]:
    """Calculates a color for every (unique) char in the input string."""
    # filter out identical chars if unique == True
    if unique:
        s = "".join(set(s))

    colors = []
    for char in s:
        hue = get_string_value(char)
        color = get_rgb_from_value(hue)
        colors.append(color)

    return colors


def get_rgb_from_value(v: float) -> Tuple[int, int, int]:
    """Returns a 3-tuple of rgb values based on the input float.

    The input float should be between 0 and 1 and is interpreted as the
    hue value in an HSL to RGB color conversion.
    """
    # colorsys returns rgb values between 0 and 1
    r, g, b = colorsys.hls_to_rgb(v, 0.5, 1)

    # multiply by 255 to get values between 0 and 255
    red = round(r * 255)
    green = round(g * 255)
    blue = round(b * 255)
    return red, green, blue


def get_string_value(s: str) -> float:
    """Calculates a float value for the given string between 0 and 1."""
    # save random state
    state = random.getstate()

    # seed random with md5sum of string
    md5sum = hashlib.md5(s.encode("utf-8")).digest()
    random.seed(md5sum)

    # get first value (reproducible because of known seed)
    value = random.random()

    # reset random state
    random.setstate(state)

    return value


class GeometricTransformation:
    """Geometric transformations from one coordinate system to another"""

    def __init__(
        self,
        input_x_axis: Tuple[float, float],
        input_y_axis: Tuple[float, float],
        output_x_axis: Tuple[float, float],
        output_y_axis: Tuple[float, float],
    ):
        """
        :param input_x_axis: The range of x values for inputs, given as a
            2-tuple with float values
        :param input_y_axis: The range of y values for inputs, given as a
            2-tuple with float values
        :param output_x_axis: The range of x values that input values are
            mapped to, given as a 2-tuple with float values
        :param output_y_axis: The range of y values that input values are
            mapped to, given as a 2-tuple with float values
        """
        self.input_x_axis = input_x_axis
        self.input_y_axis = input_y_axis
        self.output_x_axis = output_x_axis
        self.output_y_axis = output_y_axis

    def get(self, point: Tuple[float, float]) -> Tuple[float, float]:
        """Transforms a single point into the output coordinate system.

        :param point: The point to transform. Given as a 2-tuple with
            float values (x, y)
        """
        x = self.getx(point[0])
        y = self.gety(point[1])
        return x, y

    def getx(self, x: float) -> float:
        """Returns the transformed value on the x-axis for an input x"""
        input_x_min = self.input_x_axis[0]
        input_x_delta = self.input_x_axis[1] - self.input_x_axis[0]
        output_x_min = self.output_x_axis[0]
        output_x_delta = self.output_x_axis[1] - self.output_x_axis[0]

        axis_percent = (x - input_x_min) / input_x_delta
        return axis_percent * output_x_delta + output_x_min

    def gety(self, y: float) -> float:
        """Returns the transformed value on the y-axis for an input y"""
        input_y_min = self.input_y_axis[0]
        input_y_delta = self.input_y_axis[1] - self.input_y_axis[0]
        output_y_min = self.output_y_axis[0]
        output_y_delta = self.output_y_axis[1] - self.output_y_axis[0]

        axis_percent = (y - input_y_min) / input_y_delta
        return axis_percent * output_y_delta + output_y_min
