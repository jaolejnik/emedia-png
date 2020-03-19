from chunks import Chunk
from const import DISPLAY_W


def filter_method(argument):
    switcher = {
        0: "None",
        1: "Sub",
        2: "Up",
        3: "Average",
        4: "Paeth",
    }
    return switcher.get(argument, "Not found")


class IHDR(Chunk):
    def __init__(self, length, data, crc):
        super().__init__(length, "IHDR", crc)
        self.analyse(data)

    def print_info(self):
        self.basic_info()
        print(" ", end="")
        print(" HEADER DATA ".center(DISPLAY_W-2, "-"))
        print("> WIDTH:", self.width)
        print("> HEIGHT:", self.height)
        print("> BIT DEPTH:", self.bit_depth)
        print("> COLOR TYPE:", self.color_type)
        print("> FILTER METHOD:", self.filter_method)
        print("> INTERLACE METHOD:", self.interlace_method)
        print()

    def analyse(self, data):
        if self.length != 13:
            print("IHDR chunk's length is invalid")
        else:
            self.width = int.from_bytes(data[0:4], byteorder = 'big')
            self.height = int.from_bytes(data[4:8], byteorder = 'big')
            self.bit_depth = int.from_bytes(data[8:9], byteorder = 'big')
            self.color_type = int.from_bytes(data[9:10], byteorder = 'big')
            self.filter_method = filter_method(int.from_bytes(data[10:11], byteorder = 'big'))
            if int.from_bytes(data[11:12],byteorder = 'big') == 0:
                self.interlace_method = "No interlace"
            else:
                self.interlace_method = "Adam7 interlace"
