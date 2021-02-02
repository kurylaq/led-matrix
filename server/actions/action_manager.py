
from .color_wipe import ColorWipe
from .horizontal_stripes import HorizontalStripes
from .bulbasaur import Bulbasaur
from .clear import Clear
from .tetris import Tetris

from queue import Queue

class ActionManager(object):
    def __init__(self, state, matrix_args):
        super(ActionManager, self).__init__()

        self.state = state
        self.matrix_args = matrix_args
        self.curr_idx = 0
        self.current_action = None

        # action_dict will be used to call the appropriate constructor
        self.action_dict = {
            "colorWipe": ColorWipe,
            "horizontalStripes": HorizontalStripes,
            "bulbasaur": Bulbasaur,
            "clear": Clear,
            "tetris": Tetris
        }

    def receive_message(self, data):
        if ('action' in data and 'action' in self.state and data['action'] == self.state['action']) or \
                'action' not in data:
            self.update_state(data)
        else:
            # self.clear_state()
            self.update_state(data)
            self.curr_idx += 1
            self.state['idx'] = self.curr_idx
            self.start_new_action()

    def clear_state(self):
        for key in self.state.keys():
            if key != 'settings':
                del self.state[key]
        self.state['settings'].clear()

    def update_state(self, data):
        for key in data:
            if key == 'settings':
                self.state[key].update(data[key])
            elif key == 'move':
                if 'queue' not in self.state:
                    self.state['queue'] = Queue()
                self.state['queue'].put(data[key])
            else:
                self.state[key] = data[key]

    def start_new_action(self):
        if self.state['action'] in self.action_dict:
            if self.state['action'] == 'tetris':
                self.state['queue'] = Queue()
            if self.current_action is not None:
                self.current_action.terminate()
            self.current_action = self.action_dict[self.state['action']](args=[self.state, self.matrix_args, self.curr_idx])
            self.current_action.setDaemon(True)
            self.current_action.start()

            




    
