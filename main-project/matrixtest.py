import time
import argparse
import numpy as np

# from matrix import dummy_matrix
from matrix import LEDMatrix as Matrix
from image_processing import ImageProcessor

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
    """Quickly set all color values in the matrix to 0 and show"""
    for i in range(matrix.numRows()):
        for j in range(matrix.numCols()):
            matrix[i, j] = 0
    matrix.show()

def horizontalStripes(matrix, color, stripe_length=5, area_width=200, wait_ms=2):
    """Low-brightness animation to display a loop of horizontal stripes 
    travelling from left to right
    """
    
    offsets = [((43 ** i) >> 3) % area_width for i in range(matrix.numRows())]

    for i in range(area_width):
        for j, offset in enumerate(offsets):
            prevPos = (offset - 1 + area_width) % area_width
            if prevPos >= 0 and prevPos < matrix.numCols():
                matrix[j, prevPos] = 0

            for k in range(stripe_length):
                currPos = (offset + k) % area_width
                if currPos >= 0 and currPos < matrix.numCols():
                    print_color = matrix[j, currPos]
                    matrix[j, currPos] = color
            offsets[j] += 1
        
        matrix.show()
        time.sleep(wait_ms/1000.0)

def bulbasaur(matrix, image_processor, path1, path2, wait_ms=50):
    bulbasaur1 = image_processor.loadPNG(path1)
    bulbasaur2 = image_processor.loadPNG(path2)

    # print(bulbasaur1)

    for i in range(matrix.numRows()):
        for j in range(matrix.numCols()):
            matrix[i, j] = getColor(*bulbasaur1[i][j])

    matrix.show()
    time.sleep(wait_ms/1000.0)

    for i in range(matrix.numRows()):
        for j in range(matrix.numCols()):
            matrix[i, j] = getColor(*bulbasaur2[i][j])

    matrix.show()
    time.sleep(wait_ms/1000.0)



# Main program logic follows:
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-hs', '--horizontalStripes', action='store_true', help='display horizontal stripes animation')
    parser.add_argument('-cw', '--colorWipe', action='store_true', help='display color wipe animation')
    parser.add_argument('-b', '--bulbasaur', action='store_true', help='display color wipe animation')
    args = parser.parse_args()

    matrix = Matrix(NUM_ROWS, NUM_COLS, LED_PIN, brightness=LED_BRIGHTNESS)
    # Intialize the library (must be called once before other functions).
    matrix.begin()

    print ('Press Ctrl-C to quit.')

    try:
        while True:
            if (args.colorWipe):
                print("Color wipe animation")
                colorWipe(matrix, getColor(180, 0, 0))  # Red wipe
                # colorWipe(matrix, getColor(180, 0, 0))  # Red wipe
                # colorWipe(matrix, getColor(0, 180, 0))  # Green wipe
                # colorWipe(matrix, getColor(0, 0, 180))  # Blue wipe
            elif (args.horizontalStripes):
                print ('Shooting star animations')
                horizontalStripes(matrix, getColor(0, 0, 180), stripe_length=8, area_width=200, wait_ms=10)
            elif (args.bulbasaur):
                print("bulbasaur animation")
                base_path = "../images/pokemon/"
                bulbasaur(matrix, ImageProcessor(), base_path + "bulbasaur1.png", base_path + "bulbasaur2.png")

            

    except KeyboardInterrupt:
        clearMatrix(matrix)

