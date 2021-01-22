from .abstract_matrix import Matrix

try:
    from .led_matrix import LEDMatrix
except:
    print("Error importing LED matrix")

try:
    from .dummy_matrix import DummyMatrix
    from .graphics import *
except:
    print("Error importing dummy matrix")

def getColor(red, green, blue, white=0):
    """Convert the provided red, green, blue color to a 24-bit color value.
    Each color component should be a value 0-255 where 0 is the lowest intensity
    and 255 is the highest intensity.
    """

    return (int(white) << 24) | (int(red) << 16) | (int(green) << 8) | int(blue)

def getRGBValues(color):
    """Convert the unsigned integer representation of color into its red, green, 
    blue (and white) components
    """
    white = color >> 24
    red = (color >> 16) & 255
    green = (color >> 8) & 255
    blue = color & 255

    return red, green, blue, white

__all__ = ['abstract_matrix', 'dummy_matrix', 'led_matrix', 'getColor', 'getRGBValues']
