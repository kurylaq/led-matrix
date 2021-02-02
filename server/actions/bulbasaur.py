import time

from .abstract_action import Action
from .image_processing import ImageProcessor

class Bulbasaur(Action):
    def __init__(self, args=[]):
        super(Bulbasaur, self).__init__(args=args)

        self.path1 = "./images/pokemon/bulbasaur1_trans.png"
        self.path2 = "./images/pokemon/bulbasaur2_trans.png"

    def run(self):
        self.init_matrix()

        image_processor = ImageProcessor()

        bulbasaur1 = image_processor.load_png(self.path1)
        bulbasaur2 = image_processor.load_png(self.path2)

        while self.idx == self.state['idx']:
            for i in range(self.matrix.num_rows()):
                for j in range(self.matrix.num_cols()):
                   self.matrix[i, j] = self.matrix.get_color(*bulbasaur1[i][j])

            self.matrix.show()
            time.sleep(self.settings['wait_ms']/1000.0)

            if self.idx != self.state['idx']:
                return

            for i in range(self.matrix.num_rows()):
                for j in range(self.matrix.num_cols()):
                    self.matrix[i, j] = self.matrix.get_color(*bulbasaur2[i][j])

            self.matrix.show()
            time.sleep(self.settings['wait_ms']/1000.0)