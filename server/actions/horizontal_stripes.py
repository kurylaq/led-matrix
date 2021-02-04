from .abstract_action import Action
import time

class HorizontalStripes(Action):
    def __init__(self, args=[]):
        super(HorizontalStripes, self).__init__(args=args)

        default_settings = {
            'stripe_length': 5,
            'area_width': 200,
        }
        
        # replace settings with defaults if they aren't present
        for key in default_settings:
            if key not in self.settings:
                self.settings[key] = default_settings[key]

        self.area_width = self.settings['area_width']

    def main_loop(self):
        """Low-brightness animation to display a loop of horizontal stripes 
        travelling from left to right
        """
        # create offsets at beginning of animation
        offsets = [((43 ** i) >> 3) % self.area_width for i in range(self.matrix.num_rows())]

        while self.idx == self.state['idx']:
            i = 0

            for j, offset in enumerate(offsets):
                prev_pos = (offset - 1 + self.area_width) % self.area_width
                if prev_pos >= 0 and prev_pos < self.matrix.num_cols():
                    self.matrix[j, prev_pos] = 0

                for k in range(self.settings['stripe_length']):
                    curr_pos = (offset + k) % self.area_width
                    if curr_pos >= 0 and curr_pos < self.matrix.num_cols():
                        print_color = self.matrix[j, curr_pos]
                        self.matrix[j, curr_pos] = self.settings['color']
                offsets[j] += 1
            
            self.matrix.show()
            time.sleep(self.settings['wait_ms']/1000.0)
            
            i = (i + 1) % self.area_width

                
    
    
    

    