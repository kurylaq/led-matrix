from .abstract_action import Action
import time

class HorizontalStripes(Action):
    def __init__(self, args=[]):
        super(HorizontalStripes, self).__init__(args=args)

        default_settings = {
            'stripe_length': 5,
            'area_width': 200,
        }
            
        for key in default_settings:
            if key not in self.settings:
                self.settings[key] = default_settings[key]

        self.area_width = self.settings['area_width']

    def run(self):
        """Low-brightness animation to display a loop of horizontal stripes 
        travelling from left to right
        """

        self.initMatrix()
        
        offsets = [((43 ** i) >> 3) % self.area_width for i in range(self.matrix.numRows())]

        while self.idx == self.state['idx']:
            i = 0

            for j, offset in enumerate(offsets):
                prevPos = (offset - 1 + self.area_width) % self.area_width
                if prevPos >= 0 and prevPos < self.matrix.numCols():
                    self.matrix[j, prevPos] = 0

                for k in range(self.settings['stripe_length']):
                    currPos = (offset + k) % self.area_width
                    if currPos >= 0 and currPos < self.matrix.numCols():
                        print_color = self.matrix[j, currPos]
                        self.matrix[j, currPos] = self.settings['color']
                offsets[j] += 1
            
            self.matrix.show()
            time.sleep(self.settings['wait_ms']/1000.0)
            
            i = (i + 1) % self.area_width

                
    
    
    

    