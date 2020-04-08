from chunks import Chunk
from const import DISPLAY_W

def bytes_per_pixel(color_type):
    switcher = {
        0: 2,
        2: 6,
        3: 1,
    }
    return switcher[color_type]

class TRNS(Chunk):
    def __init__(self, raw_bytes, color_type, bit_depth):
        super().__init__(raw_bytes)
        self.organise_data(color_type)

    def organise_data(self, color_type):
        self.transparency_data = [self.data[i:i+bytes_per_pixel(color_type)] for i in range(0, len(self.data), bytes_per_pixel(color_type))]
        self.transparency_data = [int.from_bytes(pixel, "big") for pixel in self.transparency_data]

    def details(self):
        self.basic_info()
        print("> TRANSPARENT PIXELS:\n  [ ID: VALUE ]\n  ------------")
        for i,pixel in enumerate(self.transparency_data, 1):
            if pixel != 255: print("  * {id}: {value}".format(id=i, value=pixel))
        print()


class TEXT(Chunk):
    def __init__(self, init_data):
        if type(init_data) == list:
            super().__init__(uninit_chunk_list=init_data)
        else:
            super().__init__(raw_bytes=init_data)
        self.data_to_str()

    def data_to_str(self):
        def decode_f(x):
            return x.decode("utf-8")
        self.data = [instance.split(b"\x00") for instance in self.data]
        self.data = [list(map(decode_f, instance_split)) for instance_split in self.data]
        for instance in self.data:
            instance[0] = instance[0].upper()

    def details(self):
        self.basic_info()
        print(" ", end="")
        print(" tEXt DATA ".center(DISPLAY_W-2, "-"))
        for instance in self.data:
            print("> {keyword}: {content}".format(keyword=instance[0], content=instance[1]))
        print()
