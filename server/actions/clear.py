from .abstract_action import Action

class Clear(Action):
    def run(self):
        """Quickly set all color values in the matrix to 0 and show"""

        self.initMatrix()

        for i in range(self.matrix.numRows()):
            for j in range(self.matrix.numCols()):
                self.matrix[i, j] = 0
        self.matrix.show()