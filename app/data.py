import re
import cv2
import numpy as np
from matplotlib import pyplot as plt

from const import KILO, MEGA, GIGA, DISPLAY_W, CHUNKS
from chunks import Chunk
from ihdr import IHDR
from plte import PLTE
from idat import IDAT


def format_size(size_bytes):
    if size_bytes < KILO: return str(size_bytes) + " B"
    elif size_bytes < MEGA:
        kilo = size_bytes // KILO
        bytes = round(size_bytes % KILO, -2)
        return str(kilo) + ',' + str(bytes)[0] + " KB"
    elif size_bytes < GIGA:
        mega = size_bytes // MEGA
        kilo = round((size_bytes % MEGA) // KILO,-2)
        return str(mega) + ',' + str(kilo)[0] + " MB"


class FilePNG:
    def __init__(self, pathname):
        self.extension = "PNG"
        self.chunks = {}
        self.pathname = pathname
        self.get_name(pathname)
        self.load_data(pathname)
        self.find_chunks()
        self.init_chunks()
        # if self.chunks["IHDR"].color_type == 3:
        #     self.chunks["IDAT"].apply_palette(self.chunks["PLTE"].palettes)

    def check_ext(self, pathname):
        if pathname[-3:] != "png":
            raise Exception("INCORRECT FILE FORMAT!\nThis program is strictly for analyzing PNG files.")

    def get_name(self, pathname):
        pathname = pathname.lower()
        self.check_ext(pathname)
        fullname = re.findall('\w+.png', pathname)[0]
        self.name = fullname[:-4]

    def load_data(self, pathname):
        png_file = open(pathname, "rb")
        self.byte_data = png_file.read()
        self.size = len(self.byte_data)
        self.signature = self.byte_data[:8]
        png_file.close()

    def print_info(self):
        print(" BASIC FILE INFO ".center(DISPLAY_W, "="))
        print()
        print("> NAME:", self.name)
        print("> EXTENSION:", self.extension)
        print("> SIZE: {formatted} ({bytes} bytes)".format(formatted=format_size(self.size), bytes=self.size))
        print("> CHUNKS: ")
        for key in self.chunks_indices.keys():
            print("  ", end="")
            print(" {} ".format(key).center(DISPLAY_W-4, "-"))
            for chunk in self.chunks_indices[key].keys():
                print("  * {}".format(chunk))
        print()

    def find_chunks(self):
        found_chunks = {"CRITICAL": {}, "ANCILLARY": {}}
        i = 0
        while self.byte_data[i:i+1]:
            if 65 < self.byte_data[i] < 90 and self.byte_data[i:i+4] in CHUNKS:
                type = self.byte_data[i:i+4].decode("utf-8")
                found_chunks["CRITICAL"][type] = i-4
                i += 4
            elif 97 < self.byte_data[i] < 122 and self.byte_data[i:i+4] in CHUNKS:
                type = self.byte_data[i:i+4].decode("utf-8")
                found_chunks["ANCILLARY"][type] = i-4
                i += 4
            else:
                i += 1
        self.chunks_indices = found_chunks

    def get_chunk_data(self, chunk_type, index):
        start = index
        length = int.from_bytes(self.byte_data[start:start+4], "big")
        end = index + length + 12
        if chunk_type == "IHDR":
            self.chunks[chunk_type] = IHDR(self.byte_data[start:end])
        elif chunk_type == "PLTE":
            self.chunks[chunk_type] = PLTE(self.byte_data[start:end], self.chunks["IHDR"].color_type)
        elif chunk_type == "IDAT":
            self.chunks[chunk_type] = IDAT(self.byte_data[start:end],
                                           self.chunks["IHDR"].width,
                                           self.chunks["IHDR"].height,
                                           self.chunks["IHDR"].color_type)
        else:
            self.chunks[chunk_type] = Chunk(self.byte_data[start:end])

    def init_chunks(self):
        for chunks_dict in self.chunks_indices.values():
            for chunk in chunks_dict.keys():
                self.get_chunk_data(chunk, chunks_dict[chunk])

    def print_chunks(self):
        for chunk in self.chunks.values(): chunk.basic_info()

    def print_to_file(self):
        CRITICAL_CHUNKS = ["IHDR", "PLTE", "IDAT", "IEND"]
        new_name = "../png_files/{}_crit.png".format(self.name)
        tmp_png = open(new_name, "wb")
        tmp_png.write(self.signature)
        for chunk_type in CRITICAL_CHUNKS:
            if chunk_type in self.chunks.keys():
                tmp_png.write(self.chunks[chunk_type].raw_bytes)
        print("> Saved the file with only critical chunks to: ", new_name)
        print()

    def perform_fft(self):
        img = cv2.imread(self.pathname,0)
        f = np.fft.fft2(img)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20*np.log(np.abs(fshift))
        fig, axs = plt.subplots(1,2)
        axs[0].imshow(img, cmap = 'gray')
        axs[0].set_title("INPUT IMAGE")
        axs[0].set_axis_off()
        axs[1].imshow(magnitude_spectrum, cmap = 'gray')
        axs[1].set_title("MAGNITUDE SPECTRUM")
        axs[1].set_axis_off()
        fig.canvas.set_window_title('Fourier Transfrom')
        fig.tight_layout()
        plt.draw()
        plt.pause(0.001)
