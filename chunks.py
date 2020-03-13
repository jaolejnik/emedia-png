class Chunk:
    def __init__(self, length, type, crc):
        self.length = length
        self.type = type
        self.crc = crc

    def basic_info(self):
        print('-'*10)
        print("Type: {type}".format(type = self.type))
        print("Length: {length} bytes".format(length = self.length))
        # print("CRC: ") #don't know how to print it properly YET
