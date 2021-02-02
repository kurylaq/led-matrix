from .abstract_matrix import Matrix

try:
    from .led_matrix import LEDMatrix
except:
    print("Error importing LED matrix")

try:
    from .dummy_matrix import DummyMatrix
except:
    print("Error importing dummy matrix")

from .graphics import *

def get_color(red, green, blue, white=0):
    """Convert the provided red, green, blue color to a 24-bit color value.
    Each color component should be a value 0-255 where 0 is the lowest intensity
    and 255 is the highest intensity.
    """

    return (int(white) << 24) | (int(red) << 16) | (int(green) << 8) | int(blue)

def get_rgb_values(color):
    """Convert the unsigned integer representation of color into its red, green, 
    blue (and white) components
    """
    white = color >> 24
    red = (color >> 16) & 255
    green = (color >> 8) & 255
    blue = color & 255

    return red, green, blue, white

__all__ = ['DummyMatrix', 'LEDMatrix', 'get_color', 'get_rgb_values']
