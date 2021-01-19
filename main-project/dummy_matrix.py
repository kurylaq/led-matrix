from graphics import *
from abstract_matrix import Matrix

PIXEL_SIZE = 20

def getColor(red, green, blue, white=0):
    """Convert the provided red, green, blue color to a 24-bit color value.
    Each color component should be a value 0-255 where 0 is the lowest intensity
    and 255 is the highest intensity.
    """
    return (white << 24) | (red << 16) | (green << 8) | blue

def getRGBValues(color):
    """Convert the unsigned integer representation of color into its red, green, 
    blue (and white) components
    """
    white = color >> 24
    red = (color >> 16) & 255
    green = (color >> 8) & 255
    blue = color & 255

    return red, green, blue, white

class DummyMatrix(Matrix):
    def __init__(self, numRows, numCols, pin=18, brightness=100):
        super().__init__(numRows, numCols)
        self.win = GraphWin('Main Window', numCols * PIXEL_SIZE, numRows * PIXEL_SIZE)

        # set background to black
        self.background = Rectangle(Point(0, 0), Point(numCols * PIXEL_SIZE, numRows * PIXEL_SIZE))
        self.background.setFill(color_rgb(0, 0, 0))

        # buffer is a sparse matrix that will hold color changes between .show() calls
        self.buffer = {}
        
        # matrix will hold rectangle objects which will each represent an LED
        self.matrix = []
        for i in range(numRows):
            self.matrix.append([])
            for j in range(numCols):
                pos_x, pos_y = self.__findIndex(i, j)

                p1 = Point(pos_y + 1, pos_x + 1,)
                p2 = Point(pos_y + PIXEL_SIZE - 2, pos_x + PIXEL_SIZE - 2)
                self.matrix[i].append(Rectangle(p1, p2))
                self.matrix[i][j].setFill(color_rgb(0, 0, 0))

    def __findIndex(self, row, col):
        return row * PIXEL_SIZE, col * PIXEL_SIZE

    def __getitem__(self, index):
        color = int(self.matrix[index[0]][index[1]].config['fill'][1:], 16)
        return color
    
    def __setitem__(self, index, color):
        if index[0] in self.buffer:
            self.buffer[index[0]][index[1]] = color
        else:
            self.buffer[index[0]] = {index[1]: color}
        

    def begin(self):
        # draw background
        self.background.draw(self.win)

        # draw initially empty pixel squares
        for i in range(self.rows):
            for j in range(self.cols):
                self.matrix[i][j].draw(self.win)

    def show(self):
        # apply all changes in the buffer
        for i in self.buffer:
            for j in self.buffer[i]:
                r, g, b, _ = getRGBValues(self.buffer[i][j])
                self.matrix[i][j].setFill(color_rgb(r, g, b))

        # reset the buffer
        self.buffer = {}

    def getBrightness(self):
        return 100

    def setBrightness(self, brightness):
        return

    
