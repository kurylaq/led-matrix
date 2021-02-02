from PIL import Image
import numpy as np

class ImageProcessor:
    def __init__(self):
        pass

    def load_png(self, img_path):
        pil_img = Image.open(img_path).convert('RGB')
        np_img = np.array(pil_img)
        return np_img


