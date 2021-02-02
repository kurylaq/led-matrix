from multiprocessing import Process, Queue
from .graphics import *


PIXEL_SIZE = 20
NUM_ROWS = 26
NUM_COLS = 46

class DummyGUI(Process):
    def __init__(self, args):
        super(DummyGUI, self).__init__()
        self.queue = args[0]

        self.method_dict = {
            "begin": self.begin,
            "show": self.show,
            "terminate": self.terminate
        }

        self.should_run = True

    def run(self):
        self.win = GraphWin('Main Window', NUM_COLS * PIXEL_SIZE, NUM_ROWS * PIXEL_SIZE)

        # set background to black
        self.background = Rectangle(Point(0, 0), Point(NUM_COLS * PIXEL_SIZE, NUM_ROWS * PIXEL_SIZE))
        self.background.setFill(color_rgb(0, 0, 0))
        
        # matrix will hold rectangle objects which will each represent an LED
        self.matrix = []

        for i in range(NUM_ROWS):
            self.matrix.append([])
            for j in range(NUM_COLS):
                pos_x, pos_y = i * PIXEL_SIZE, j * PIXEL_SIZE

                p1 = Point(pos_y + 1, pos_x + 1,)
                p2 = Point(pos_y + PIXEL_SIZE - 2, pos_x + PIXEL_SIZE - 2)
                self.matrix[i].append(Rectangle(p1, p2))
                self.matrix[i][j].setFill(color_rgb(0, 0, 0))

        while self.should_run:
            msg = self.queue.get()
            if msg[0] in self.method_dict:
                args = () if len(msg) < 2 else msg[1]
                self.method_dict[msg[0]](*args)


    def get_rgb_values(self, color):
        """Convert the unsigned integer representation of color into its red, green, 
        blue (and white) components
        """
        white = color >> 24
        red = (color >> 16) & 255
        green = (color >> 8) & 255
        blue = color & 255

        return red, green, blue, white

    def begin(self):
        # draw background
        self.background.draw(self.win)

        # draw initially empty pixel squares
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                self.matrix[i][j].draw(self.win)

    def show(self, buffer):
        # apply all changes in the buffer
        for i in buffer:
            for j in buffer[i]:
                r, g, b, _ = self.get_rgb_values(buffer[i][j])
                self.matrix[i][j].setFill(color_rgb(r, g, b))

    def terminate(self):
        self.should_run = False
