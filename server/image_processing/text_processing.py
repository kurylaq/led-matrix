from PIL import Image, ImageDraw, ImageFont
import numpy as np
import math

FONTS = {
    "tiny_islanders": {
        "height": 14,
        "file": "TinyIslanders-nOYg.ttf"
    },
    "teeny_tiny_pixls": {
        "height": 5,
        "file": "TeenyTinyPixls-o2zo.ttf"
    },
    "pixeboy": {
        "height": 10,
        "file": "Pixeboy-z8XGD.ttf"
    }
}

class TextProcessor:
    def __init__(self):
        self.fonts = FONTS

    def get_single_line_text_array(self, text, font_name='teeny_tiny_pixls'):
        # create an image
        out = Image.new("RGB", (46, 26))

        # get a font
        fnt = ImageFont.truetype('./fonts/' + self.fonts[font_name]['file'], self.fonts[font_name]['height'])
        # get a drawing context
        d = ImageDraw.Draw(out)

        # draw multiline text
        d.text((0, 0), text, fill=(255, 255, 255), font=fnt)

        np_img = np.array(out)

        min_x, min_y, max_x, max_y = math.inf, math.inf, -math.inf, -math.inf

        for i, row in enumerate(np_img):
            for j, color in enumerate(row):
                if sum(color) != 0:
                    min_x, max_x = min(min_x, j), max(max_x, j)
                    min_y, max_y = min(min_y, i), max(max_y, i)
                    
        return np_img[min_y:max_y + 1, min_x:max_x + 1]

    def get_multiline_text_array(self, text, font_name='teeny_tiny_pixls'):
        line_list = []

        for line in text.splitlines():
            line_list.append(self.get_single_line_text_array(line, font_name))

        return line_list

    def draw_text_arr(self, matrix, text_arr, separation=2, start_pos=(0, 0)):
        height = len(text_arr[0])
        for num, line in enumerate(text_arr):
            for i, row in enumerate(line):
                for j, color in enumerate(row):
                    matrix[start_pos[0] + num * (height + separation) + i, start_pos[1] + j] = matrix.get_color(*color)