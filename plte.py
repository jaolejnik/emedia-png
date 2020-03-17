from chunks import Chunk
import numpy as np
import matplotlib.pyplot as plt


def init_palette():
    palette = {"Red": {}, "Green": {}, "Blue": {}}
    for color in palette.keys():
        for i in range(256):
            palette[color][i] = 0
    return palette


class PLTE(Chunk):
    def __init__(self, length, data, crc, color_type):
        super().__init__(length, "PLTE", crc)
        self.entries = length/3
        self.required = True if color_type == 3 else False
        self.palette = init_palette()
        self.fill_palette(data)

    def fill_palette(self, data):
        for i in range(0, self.length, 3):
            self.palette["Red"][data[i]] += 1
            self.palette["Green"][data[i+1]] += 1
            self.palette["Blue"][data[i+2]] += 1

    def print_palette(self):
        print("Palette:")
        for color in self.palette.keys():
            print("   {color}:".format(color=color))
            for i in range(256):
                if self.palette[color][i] == 0: continue
                print("         {key}: {value}".format(key=i, value=self.palette[color][i]))

    def plot_palette(self):
        max_y = 0
        for color in self.palette.keys():
            if max(self.palette[color].values()) > max_y:
                max_y = max(self.palette[color].values())
        yticks = np.arange(0, max_y+1, 1)
        fig, axs = plt.subplots(1,3)
        plot_colors = ['r', 'g', 'b']
        for i,color in enumerate(self.palette.keys()):
            axs[i].set_yticks(yticks)
            axs[i].set_ylim(0, max_y+1)
            axs[i].set_xlim(0, 256)
            axs[i].bar(self.palette[color].keys(), self.palette[color].values(), width=5, color=plot_colors[i])
            axs[i].grid(axis='y', alpha=0.2)
        plt.show()

    def print_info(self):
        self.basic_info()
