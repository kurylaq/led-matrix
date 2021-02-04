from image_processing import TextProcessor
from .abstract_action import Action

class Text(Action):
    def __init__(self, args=[]):
        super(Text, self).__init__(args)
        self.text = "a"
        self.text_processor = TextProcessor()

    def main_loop(self):
        while self.state['idx'] == self.idx:
            if self.state['text'] != self.text:
                self.clear_matrix()

                self.text = self.state['text']
                arr = self.text_processor.get_multiline_text_array(self.text)
                self.text_processor.draw_text_arr(self.matrix, arr)
                self.matrix.show()
                
                
