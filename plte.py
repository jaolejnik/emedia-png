from chunks import Chunk
import numpy as np
import matplotlib.pyplot as plt
import colorsys


def init_palette():
    palette = {"Red": {}, "Green": {}, "Blue": {}}
    for color in palette.keys():
        for i in range(256):
            palette[color][i] = 0
    return palette

def translate(value, from_min, from_max, to_min, to_max):
    num = (value - from_min) * (to_max - to_min)
    den = from_max - from_min
    return to_min + num/den

def translate_RGB(rgb_tuple):
    translated_red = translate(rgb_tuple[0], 0, 255, 0, 1)
    translated_green = translate(rgb_tuple[1], 0, 255, 0, 1)
    translated_blue = translate(rgb_tuple[2], 0, 255, 0, 1)
    return (translated_red, translated_green, translated_blue)


class PLTE(Chunk):
    def __init__(self, length, data, crc, color_type):
        super().__init__(length, "PLTE", crc)
        # print(length/3)
        self.entries = length//3
        self.required = True if color_type == 3 else False
        self.palettes = [(data[i], data[i+1], data[i+2]) for i in range(0, self.length, 3)]

    def plot_palettes(self):
        fig, ax = plt.subplots(1, 1)
        ax.set_xlim(0, self.entries)
        ax.set_ylim(0, 1)
        for i in range(self.entries):
            ax.bar(i, 1, width=1, color=translate_RGB(self.palettes[i]))
        ax.set_axis_off()
        fig.tight_layout()
        fig.canvas.set_window_title('Palettes')
        plt.show()

    def print_info(self):
        self.basic_info()
