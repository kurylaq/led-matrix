import time

from ..abstract_action import Action
from ..image_processing import ImageProcessor
from .tetris_board import TetrisBoard
from queue import Queue

class Tetris(Action):
    def __init__(self, args=[]):
        super(Tetris, self).__init__(args=args)

        if 'queue' not in self.state:
            self.state['queue'] = Queue()
        
        self.queue = self.state['queue']
        

    def run(self):
        self.init_matrix()
        self.board = TetrisBoard(self.matrix)
        self.board.draw_frame()
        self.board.drop_random_piece()

        while self.idx == self.state['idx']:
            end_time = round(time.time() * 1000 + self.settings['wait_ms']) 
            while round(time.time() * 1000) < end_time:
                if not self.queue.empty():
                    motion = self.queue.get()
                    if motion == 'right':
                        self.board.move_sideways('r')
                    elif motion == 'left':
                        self.board.move_sideways('l')
                    elif motion == 'up':
                        self.board.rotate()
                    elif motion == 'down':
                        self.board.drop_down()
            # Once the waiting time has passed, move the piece down if
            # the user didn't hit down
            if self.board.game_over or self.board.move_down() == 0:
                break
