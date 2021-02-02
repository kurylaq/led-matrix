from abc import ABC, abstractmethod

class Matrix(ABC):
    def __init__(self, num_rows, num_cols, pin=18, brightness=100):
        self.rows = num_rows
        self.cols = num_cols

    def get_color(self, red, green, blue, white=0):
        """Convert the provided red, green, blue color to a 24-bit color value.
        Each color component should be a value 0-255 where 0 is the lowest intensity
        and 255 is the highest intensity.
        """

        return (int(white) << 24) | (int(red) << 16) | (int(green) << 8) | int(blue)

    def get_rgb_values(self, color):
        """Convert the unsigned integer representation of color into its red, green, 
        blue (and white) components
        """
        white = color >> 24
        red = (color >> 16) & 255
        green = (color >> 8) & 255
        blue = color & 255

        return red, green, blue, white

    @abstractmethod
    def __getitem__(self, index):
        """Get the color at index (row, col)"""
        pass
    
    @abstractmethod
    def __setitem__(self, index, color):
        """Set the color at index (row, col) to color"""
        pass

    @abstractmethod
    def begin(self):
        """Initialize the matrix along w/ necessary libraries"""
        pass

    @abstractmethod
    def show(self):
        """Display changes in LED colour and brightness"""
        pass

    @abstractmethod
    def get_brightness(self):
        """Get LED brightness cap"""
        pass
    
    @abstractmethod
    def set_brightness(self, brightness):
        """Set LED brightness cap"""
        pass

    def num_rows(self):
        """Return total number of rows"""
        return self.rows
    
    def num_cols(self):
        """Return total number of columns"""
        return self.cols

    
