from .abstract_action import Action

class Clear(Action):
    def run(self):
        """Quickly set all color values in the matrix to 0 and show"""

        self.init_matrix()

        for i in range(self.matrix.num_rows()):
            for j in range(self.matrix.num_cols()):
                self.matrix[i, j] = 0
                
        self.matrix.show()
        self.matrix.terminate()