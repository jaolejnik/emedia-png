from chunks import Chunk


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
        self.fill_pallete(data)

    def fill_pallete(self, data):
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

    def print_info(self):
        self.basic_info()
