from .abstract_action import Action

class Clear(Action):
    def main_loop(self):
        """Quickly set all color values in the matrix to 0 and show"""
        self.clear_matrix()

    