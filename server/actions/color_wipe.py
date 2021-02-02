from .abstract_action import Action
import time

class ColorWipe(Action):
    def run(self):
        """Wipe color across display a pixel at a time."""

        self.init_matrix()

        while self.idx == self.state['idx']:
            for i in range(self.matrix.num_rows()):
                for j in range(self.matrix.num_cols()):
                    self.matrix[i, j] = self.settings['color']
                    self.matrix.show()
                    time.sleep(self.settings['wait_ms'] / 1000.0)

                    if self.idx != self.state['idx']:
                        return