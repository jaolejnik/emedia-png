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

# TODO
# def chunk_switch(chunk_type, length, data, crc):
#     switcher = {
#     "IHDR": IHDR,
#     "PLTE": PLTE,
#     }
#     return switcher.get(chunk_type, Chunk)(length, data, crc)

class FilePNG:
    def __init__(self, pathname):
        self.extension = "PNG"
        self.chunks = {}
        self.get_name(pathname)
        self.load_data(pathname)
        self.find_chunks()
        self.init_chunks()

    def check_ext(self, pathname):
        if pathname[-3:].lower() != "png":
            raise Exception("INCORRECT FILE FORMAT!\nThis program is strictly for analyzing PNG files.")

    def get_name(self, pathname):
        self.check_ext(pathname)
        self.name = pathname[10:-4]

    def load_data(self, pathname):
        png_file = open(pathname, "rb")
        self.byte_data = png_file.read()
        self.size = len(self.byte_data)
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

    def find_chunks(self):
        found_chunks = {"CRITICAL": {}, "ANCILLARY": {}}
        i = 0
        while self.byte_data[i:i+1]:
            if 65 < self.byte_data[i] < 90 and self.byte_data[i:i+4] in CHUNKS:
                type = self.byte_data[i:i+4].decode("utf-8")
                found_chunks["CRITICAL"][type] = i
                i += 4
            elif 97 < self.byte_data[i] < 122 and self.byte_data[i:i+4] in CHUNKS:
                type = self.byte_data[i:i+4].decode("utf-8")
                found_chunks["ANCILLARY"][type] = i
                i += 4
            else:
                i += 1
        self.chunks_indices = found_chunks

    def get_chunk_data(self, chunk_type, index):
        if chunk_type == "IEND":
            self.chunks["IEND"] = Chunk(0, "IEND", None)
        else:
            length = int.from_bytes(self.byte_data[index-4:index], "big")
            index += 4
            data = self.byte_data[index:index+length]
            index += length
            crc = self.byte_data[index:index+4]
            if chunk_type == "IHDR":            # temporary solution -> switcher TODO
                self.chunks[chunk_type] = IHDR(length, data, crc)
            elif chunk_type == "PLTE":
                self.chunks[chunk_type] = PLTE(length, data, crc, self.chunks["IHDR"].color_type)
            elif chunk_type == "IDAT":
                self.chunks[chunk_type] = IDAT(length, data, crc, self.chunks["IHDR"].width, self.chunks["IHDR"].height, self.chunks["IHDR"].color_type)
            else:
                self.chunks[chunk_type] = Chunk(length, chunk_type, crc)

    def init_chunks(self):
        for chunks_dict in self.chunks_indices.values():
            for chunk in chunks_dict.keys():
                self.get_chunk_data(chunk, chunks_dict[chunk])

    def print_chunks(self):
        for chunk in self.chunks.values(): chunk.basic_info()
        # self.chunks["PLTE"].plot_palettes()
        self.chunks["IHDR"].print_info()
        if self.chunks["IHDR"].color_type == 3:
            self.chunks["IDAT"].apply_palette(self.chunks["PLTE"].palettes)
        self.chunks["IDAT"].check_correctness()
