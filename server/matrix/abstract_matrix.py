from abc import ABC, abstractmethod

class Matrix(ABC):
    def __init__(self, numRows, numCols, pin=18, brightness=100):
        self.rows = numRows
        self.cols = numCols

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

    
