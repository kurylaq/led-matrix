try:
    from rpi_ws281x import *
    from .abstract_matrix import Matrix

    class LEDMatrix(Matrix):
        def __init__(self, num_rows, num_cols, pin=18, brightness=100):
            super().__init__(num_rows, num_cols)
            self.strip = Adafruit_NeoPixel(num_rows * num_cols, pin, brightness=brightness)

        def __findIndex(self, row, col):
            idx = 1196 - 46 * (row + 1)

            if row % 2 == 0:
                idx += col
            else:
                idx += 45 - col

            return idx

        def __getitem__(self, index):
            idx = self.__findIndex(index[0], index[1])
            return self.strip.getPixelColor(idx)
        
        def __setitem__(self, index, color):
            idx = self.__findIndex(index[0], index[1])
            self.strip.setPixelColor(idx, color)

        def begin(self):
            self.strip.begin()

        def show(self):
            self.strip.show()

        def get_brightness(self):
            return self.strip.get_brightness()

        def set_brightness(self, brightness):
            self.strip.set_brightness(brightness)
except:
    print("rpi_ws281x not found")

    
