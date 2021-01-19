from PIL import Image
import numpy as np

class ImageProcessor:
    def __init__(self):
        pass

    def loadPNG(self, img_path):
        pil_img = Image.open(img_path)
        np_img = np.array(pil_img)
        return np_img


