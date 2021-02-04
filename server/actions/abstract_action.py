try:
    from matrix import LEDMatrix as Matrix
except:
    from matrix import DummyMatrix as Matrix

from matrix import get_color, get_rgb_values

from threading import Thread

class Action(Thread):
    def __init__(self, args=[]):
        super(Action, self).__init__()
        self.state = args[0]
        self.settings = self.state['settings']
        self.matrix_args = args[1]
        self.idx = args[2]

        default_settings = {
            'color': get_color(30, 0, 180),
            'wait_ms': 500,
        }
            
        for key in default_settings:
            if key not in self.settings:
                self.settings[key] = default_settings[key]

    def run(self):
        self.matrix = Matrix(*self.matrix_args)
        self.matrix.begin()
        self.main_loop()
        self.matrix.terminate()

    def main_loop(self):
        pass

    def clear_matrix(self):
        for i in range(self.matrix.num_rows()):
            for j in range(self.matrix.num_cols()):
                self.matrix[i, j] = 0

    def terminate(self):
        if self.matrix is not None:
            self.matrix.terminate()
