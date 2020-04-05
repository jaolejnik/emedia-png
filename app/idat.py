from chunks import Chunk
from ihdr import IHDR
import zlib
import matplotlib.pyplot as plt
import numpy as np

def bytes_per_pixel(argument):
    switcher = {
        0: 1,
        2: 3,
        3: 1,
        4: 2,
        6: 4,
    }
    return switcher.get(argument, "Not found")

class IDAT(Chunk):
    def __init__(self, raw_bytes, width, height, color_type):
        super().__init__(raw_bytes)
        self.width = width
        self.height = height
        self.color_type = color_type
        self.bytes_per_pixel = bytes_per_pixel(color_type)
        self.analyse()

    def analyse(self):
        self.data = zlib.decompress(self.data)
        self.reconstructed_data = []
        stride = self.width * self.bytes_per_pixel
        i = 0
        for r in range(self.height):
            filter_type = self.data[i]
            i += 1
            for c in range(stride):
                filt_x = self.data[i]
                i += 1
                if filter_type == 0:
                    recon_x  = filt_x
                elif filter_type == 1:
                    recon_x = filt_x + self.reconstruction_a(r, c, stride)
                elif filter_type == 2:
                    recon_x = filt_x + self.reconstruction_b(r, c, stride)
                elif filter_type == 3:
                    recon_x = filt_x + (self.reconstruction_a(r, c, stride)
                     + self.reconstruction_b(r, c, stride)) // 2
                elif filter_type == 4:
                    recon_x = filt_x + self.paeth_predictor(self.reconstruction_a(r, c, stride),
                     self.reconstruction_b(r, c, stride), self.reconstruction_c(r, c, stride))
                else:
                    raise Exception("unknown filter type: " + str(filter_type))
                self.reconstructed_data.append(recon_x & 0xff) #truncation to byte

    def paeth_predictor(self, a, b, c):
        p = a + b - c
        pa = abs(p - a)
        pb = abs(p - b)
        pc = abs(p - c)
        if pa <= pb and pa <= pc:
            Pr = a
        elif pb <= pc:
            Pr = b
        else:
            Pr = c
        return Pr

    def reconstruction_a(self, r, c, stride):
        if c >= self.bytes_per_pixel:
            return self.reconstructed_data[r * stride + c - self.bytes_per_pixel]
        else:
            return 0

    def reconstruction_b(self, r, c, stride):
        if r > 0:
            return self.reconstructed_data[(r-1) * stride + c]
        else:
            return 0

    def reconstruction_c(self, r, c, stride):
        if r > 0 and c >= self.bytes_per_pixel:
            return self.reconstructed_data[(r-1) * stride + c - self.bytes_per_pixel]
        else:
            return 0

    def apply_palette(self, palette):
        self.reconstructed_data = [pixel for pixel_i in self.reconstructed_data for pixel in palette[pixel_i]]
        self.bytes_per_pixel = 3

    def print_info(self):
        self.basic_info()

    def details(self):
        plt.imshow(np.array(self.reconstructed_data).reshape((self.height, self.width, self.bytes_per_pixel)))
        plt.show()
