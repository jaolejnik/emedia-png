from const import DISPLAY_W

class Chunk:
    def __init__(self, raw_bytes):
        self.raw_bytes = raw_bytes
        self.init_fields()

    def init_fields(self):
        i = 0
        self.length = int.from_bytes(self.raw_bytes[i:i+4], "big")
        i += 4
        self.type = self.raw_bytes[i:i+4].decode("utf-8")
        i += 4
        self.data = self.raw_bytes[i:i+self.length]
        i += self.length
        self.crc = self.raw_bytes[i:i+4]

    def basic_info(self):
        print(" {type} CHUNK ".format(type=self.type).center(DISPLAY_W, "="))
        print(" ", end="")
        print(" BASIC INFO ".center(DISPLAY_W-2, "-"))
        print("> TYPE:", self.type)
        print("> LENGTH: {length} bytes".format(length = self.length))
        print("> CRC: ", self.crc)
        print()

    def details(self):
        print("> None defined for this chunk (yet).")
        print()
