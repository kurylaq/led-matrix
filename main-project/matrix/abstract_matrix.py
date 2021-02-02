from abc import ABC, abstractmethod

class Matrix(ABC):
    def __init__(self, num_rows, num_cols, pin=18, brightness=100):
        self.rows = num_rows
        self.cols = num_cols

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

    
