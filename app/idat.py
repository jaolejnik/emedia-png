import zlib
import matplotlib.pyplot as plt
import numpy as np

from chunks import Chunk
from ihdr import IHDR


def bytes_per_pixel(color_type):
    switcher = {
        0: 1,
        2: 3,
        3: 1,
        4: 2,
        6: 4,
    }
    return switcher.get(color_type, "Not found")


class IDAT(Chunk):
    '''
    IDAT contains encoded and filtered actual image data.
    To get back raw pixel data we should reverse this process.
    '''
    def __init__(self, init_data, width, height, color_type):
        if type(init_data) == list:
            super().__init__(uninit_chunk_list=init_data)
        else:
            super().__init__(raw_bytes=init_data)
        if type(self.data) == list:
            self.length = sum(self.length)
            self.data = b"".join(self.data)
        self.width = width
        self.height = height
        self.color_type = color_type
        self.bytes_per_pixel = bytes_per_pixel(color_type)
        self.analyse()

    def analyse(self):
        '''
        At first pixel data are decompressed with zlib's module, then each
        scanline prefixed with a byte indicating which filter type was used to
        filter is unfiltered with correct filter type.
        '''
        self.compressed_data = bytearray(self.data)
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
        '''
        Method to filter pixel data specified with filter type
        number 4 - Paeth.
        '''
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

    def display_data(self, title, data=None, bytes_per_pixel=None):
        if data == None: data = self.reconstructed_data
        fig, ax = plt.subplots(1, 1)
        if bytes_per_pixel == None: bytes_per_pixel = self.bytes_per_pixel
        if bytes_per_pixel == 1:
            ax.imshow(np.array(data).reshape((self.height, self.width)), cmap="gray")
        else:
            ax.imshow(np.array(data).reshape((self.height, self.width, bytes_per_pixel)))
        ax.set_axis_off()
        ax.set_facecolor("whitesmoke")
        fig.patch.set_facecolor("whitesmoke")
        fig.tight_layout()
        fig.canvas.set_window_title(title)
        plt.draw()
        plt.show()
        plt.pause(0.001)

    def apply_palette(self, palette):
        new_data = [pixel for pixel_i in self.reconstructed_data for pixel in palette[pixel_i]]
        self.display_data("IDAT + palettes", data=new_data, bytes_per_pixel=3)

    def apply_transparency(self, transparency_data, palette=None):
        if palette != None:
            transparent_palette = []
            for i in range(len(palette)):
                if i > len(transparency_data)-1:
                    transparent_palette.append((palette[i][0],
                                                palette[i][1],
                                                palette[i][2],
                                                255))
                else:
                    transparent_palette.append((palette[i][0],
                                                palette[i][1],
                                                palette[i][2],
                                                transparency_data[i]))
            new_data = [pixel for pixel_i in self.reconstructed_data for pixel in transparent_palette[pixel_i]]
            self.display_data("IDAT + palette + transparency", data=new_data, bytes_per_pixel=4)
        print("> The palette and transparency has been applied!\n")


    def details(self):
        '''
        Prints chunk's details into stdout.
        '''
        self.basic_info()
        self.display_data("IDAT")
