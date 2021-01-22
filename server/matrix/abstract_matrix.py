from abc import ABC, abstractmethod

class Matrix(ABC):
    def __init__(self, numRows, numCols, pin=18, brightness=100):
        self.rows = numRows
        self.cols = numCols

    def getColor(self, red, green, blue, white=0):
        """Convert the provided red, green, blue color to a 24-bit color value.
        Each color component should be a value 0-255 where 0 is the lowest intensity
        and 255 is the highest intensity.
        """
        return (white << 24) | (red << 16) | (green << 8) | blue

    def getRGBValues(self, color):
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
    def getBrightness(self):
        """Get LED brightness cap"""
        pass
    
    @abstractmethod
    def setBrightness(self, brightness):
        """Set LED brightness cap"""
        pass

    def numRows(self):
        """Return total number of rows"""
        return self.rows
    
    def numCols(self):
        """Return total number of columns"""
        return self.cols

    
