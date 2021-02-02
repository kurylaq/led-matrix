from .graphics import *
from .abstract_matrix import Matrix
from .dummy_gui import DummyGUI

from multiprocessing import Manager, Queue

PIXEL_SIZE = 20

class DummyMatrix(Matrix):
    def __init__(self, num_rows, num_cols, pin=18, brightness=100):
        super().__init__(num_rows, num_cols)
        self.queue = Queue()
        self.manager = Manager()
        self.buffer = {}
        
        # matrix will hold rectangle objects which will each represent an LED
        self.matrix = []
        for _ in range(num_rows):
            self.matrix.append([0 for _ in range(num_cols)])

        
        self.dummy_gui = DummyGUI([self.queue])
        self.dummy_gui.start()

    def __getitem__(self, index):
        return self.matrix[index[0]][index[1]]

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

    def begin(self):
        self.queue.put(("begin", ))

    def show(self):
        # apply all changes in the buffer
        for i in self.buffer:
            for j in self.buffer[i]:
                self.matrix[i][j] = self.buffer[i][j]

        self.queue.put(("show", (self.buffer, )))

        self.buffer = {}

    def get_brightness(self):
        return 100

    def set_brightness(self, brightness):
        return

    def terminate(self):
        self.queue.put(("terminate", ))

    
