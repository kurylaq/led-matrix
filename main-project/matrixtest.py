import time
import argparse
from matrix import Matrix

# LED Matrix configuration:
NUM_ROWS       = 26      # Number of rows in our LED Matrix
NUM_COLS       = 46      # Number of columns in our LED Matrix
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0)
LED_BRIGHTNESS = 50 

def getColor(red, green, blue, white=0):
    """Convert the provided red, green, blue color to a 24-bit color value.
    Each color component should be a value 0-255 where 0 is the lowest intensity
    and 255 is the highest intensity.
    """
    return (white << 24) | (red << 16) | (green << 8) | blue

def getRGBValues(color):
    """Convert the unsigned integer representation of color into its red, green, 
    blue (and white) components
    """
    white = color >> 24
    red = (color >> 16) & 255
    green = (color >> 8) & 255
    blue = color & 255

    return red, green, blue, white

# Define functions which animate LEDs in various ways.
def colorWipe(matrix, color, wait_ms=2):
    """Wipe color across display a pixel at a time."""
    for i in range(matrix.numRows()):
        for j in range(matrix.numCols()):
            matrix[i, j] = color
            matrix.show()
            time.sleep(wait_ms/1000.0)

def clearMatrix(matrix):
    for i in range(matrix.numRows()):
        for j in range(matrix.numCols()):
            matrix[i, j] = 0
    matrix.show()

# Main program logic follows:
if __name__ == '__main__':
    matrix = Matrix(NUM_ROWS, NUM_COLS, LED_PIN, brightness=LED_BRIGHTNESS)
    # Intialize the library (must be called once before other functions).
    matrix.begin()

    print ('Press Ctrl-C to quit.')

    try:
        while True:
            print ('Color wipe animations.')
            colorWipe(matrix, getColor(180, 0, 0))  # Red wipe
            colorWipe(matrix, getColor(0, 180, 0))  # Blue wipe
            colorWipe(matrix, getColor(0, 0, 180))  # Green wipe
            #print ('Theater chase animations.')
            #theaterChase(strip, Color(127, 127, 127))  # White theater chase
            #theaterChase(strip, Color(127,   0,   0))  # Red theater chase
            #theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
            # print ('Rainbow animations.')
            #rainbow(strip)
            # rainbowCycle(strip)
            # theaterChaseRainbow(strip)

    except KeyboardInterrupt:
        clearMatrix(matrix)

