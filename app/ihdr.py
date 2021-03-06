from chunks import Chunk
from const import DISPLAY_W

def filter_method(argument):
    '''
    Method for parametrization filter methods that can reach in IHDR chunk
    The argument of this method is 1 byte located in IHDR chunk.
    '''
    switcher = {
        0: "None",
        1: "Sub",
        2: "Up",
        3: "Average",
        4: "Paeth",
    }
    return switcher.get(argument, "Not found")


class IHDR(Chunk):
    '''
    IHDR chunk contains important informations about image such as
    width, height, bitdepth, colortype compression Method, filter method,
    interlace method.
    '''
    def __init__(self, raw_bytes):
        super().__init__(raw_bytes)
        self.analyse()

    def details(self):
        '''
        Prints chunk's details into stdout.
        '''
        self.basic_info()
        print(" ", end="")
        print(" HEADER DATA ".center(DISPLAY_W-2, "-"))
        print("> WIDTH:", self.width)
        print("> HEIGHT:", self.height)
        print("> BIT DEPTH:", self.bit_depth)
        print("> COLOR TYPE:", self.color_type)
        print("> COMPRESSION METHOD:", self.compression_method)
        print("> FILTER METHOD:", self.filter_method)
        print("> INTERLACE METHOD:", self.interlace_method)
        print()

    def analyse(self):
        '''
        Method for analysing bytes contained in IHDR Chunk byte-for-byte.
        '''
        if self.length != 13:
            print(self.length)
            raise Exception("IHDR chunk's length is invalid")
        else:
            self.width = int.from_bytes(self.data[0:4], byteorder = 'big')
            self.height = int.from_bytes(self.data[4:8], byteorder = 'big')
            self.bit_depth = int.from_bytes(self.data[8:9], byteorder = 'big')
            self.color_type = int.from_bytes(self.data[9:10], byteorder = 'big')
            self.compression_method = int.from_bytes(self.data[10:11], byteorder = 'big')
            self.filter_method = filter_method(int.from_bytes(self.data[11:12], byteorder = 'big'))
            if int.from_bytes(self.data[12:13],byteorder = 'big') == 0:
                self.interlace_method = "No interlace"
            else:
                self.interlace_method = "Adam7 interlace"
