import time
import argparse
from multiprocessing import Pipe

from connection_manager import ConnectionManagerProcess
from state_manager import StateManager
from actions import ActionManager

# LED Matrix configuration:
NUM_ROWS       = 26      # Number of rows in our LED Matrix
NUM_COLS       = 46      # Number of columns in our LED Matrix
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0)
LED_BRIGHTNESS = 150 

if __name__ == '__main__':
    try:
        parent_conn, child_conn = Pipe()
        p = ConnectionManagerProcess(child_conn)

        state = {}
        state['settings'] = {}

        matrix_args = (NUM_ROWS, NUM_COLS, LED_PIN, LED_BRIGHTNESS)
        
        action_manager = ActionManager(state, matrix_args)

        p.start()

        while True:
            data = parent_conn.recv()
            if data is not None:
                action_manager.receive_message(data)

        p.join()

    except KeyboardInterrupt:
        parent_conn.send(("stop", ))
        # parent_conn.close()
