
from .color_wipe import ColorWipe
from .horizontal_stripes import HorizontalStripes
from .bulbasaur import Bulbasaur
from .clear import Clear

class ActionManager(object):
    def __init__(self, state, matrix_args):
        super(ActionManager, self).__init__()

        self.state = state
        self.matrix_args = matrix_args
        self.curr_idx = 0
        self.currentAction = None

        # actionDict will be used to call the appropriate constructor
        self.actionDict = {
            "colorWipe": ColorWipe,
            "horizontalStripes": HorizontalStripes,
            "bulbasaur": Bulbasaur,
            "clear": Clear,
        }

    def receiveMessage(self, data):
        if ('action' in data and 'action' in self.state and data['action'] == self.state['action']) or \
                'action' not in data:
            self.updateState(data)
        else:
            self.clearState()
            self.updateState(data)
            self.curr_idx += 1
            self.state['idx'] = self.curr_idx

            if 'action' in self.state:
                self.startNewAction()

    def clearState(self):
        for key in self.state.keys():
            if key != 'settings':
                del self.state[key]
        self.state['settings'].clear()

    def updateState(self, data):
        for key in data:
            if key == 'settings':
                self.state[key].update(data[key])
            else:
                self.state[key] = data[key]

    def startNewAction(self):
        if self.state['action'] in self.actionDict:
            self.currentAction = self.actionDict[self.state['action']](args=[self.state, self.matrix_args, self.curr_idx])
            self.currentAction.start()

            




    
