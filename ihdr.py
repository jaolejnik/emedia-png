from chunks import Chunk


class IHDR(Chunk):
    def __init__(self, length, data, crc):
        super().__init__(length, "IHDR", crc)
        self.analyse(data)

    def print_info(self):
        self.basic_info()
        print("Width: {width}\nHeight: {height}".format(width = self.width, height = self.height))
        print("Bit depth: {bit_depth}\nColor type: {color_type}".format(bit_depth = self.bit_depth, color_type = self.color_type))
        print("Filter method: {filter_method}".format(filter_method = self.filter_method))
        print("Interlace method: {interlace_method}".format(interlace_method = self.interlace_method))

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

def filter_method(argument):
    switcher = {
        0: "None",
        1: "Sub",
        2: "Up",
        3: "Average",
        4: "Paeth",
    }
    return switcher.get(argument, "Not found")
