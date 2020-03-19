from const import DISPLAY_W


class Chunk:
    def __init__(self, length, type, crc):
        self.length = length
        self.type = type
        self.crc = crc

    def basic_info(self):
        print(" {type} CHUNK ".format(type=self.type).center(DISPLAY_W, "="))
        print(" ", end="")
        print(" BASIC INFO ".center(DISPLAY_W-2, "-"))
        print("> TYPE:", self.type)
        print("> LENGTH: {length} bytes".format(length = self.length))
        # print("CRC: ") #don't know how to print it properly YET
