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

def shootingStars(matrix, color, length=200, wait_ms=2):
    offsets = [((43 ** i) >> 3) % length for i in range(matrix.numRows())]

    for i in range(length):
        for j in range(matrix.numRows()):
            for k in range(matrix.numCols()):
                matrix[j, k] = 0

        for j, offset in enumerate(offsets):
            for k in range(5):
                currPos = (offset + k) % length
                if currPos >= 0 and currPos < matrix.numCols():
                    matrix[j, currPos] = color
            offsets[j] += 1
        
        matrix.show()
        time.sleep(wait_ms/1000.0)



# Main program logic follows:
if __name__ == '__main__':
    matrix = Matrix(NUM_ROWS, NUM_COLS, LED_PIN, brightness=LED_BRIGHTNESS)
    # Intialize the library (must be called once before other functions).
    matrix.begin()

    print ('Press Ctrl-C to quit.')

    try:
        while True:
            print ('Shooting star animations.')
            # colorWipe(matrix, getColor(180, 0, 0))  # Red wipe
            # colorWipe(matrix, getColor(0, 180, 0))  # Green wipe
            # colorWipe(matrix, getColor(0, 0, 180))  # Blue wipe
            shootingStars(matrix, getColor(0, 0, 180))

    except KeyboardInterrupt:
        clearMatrix(matrix)

