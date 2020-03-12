class Chunk:
    def __init__(self, length, type, data, crc):
        self.length = length
        self.type = type
        self.data = data
        self.crc = crc

    def print_info(self):
        print('-'*10)
        print("Type: {type}".format(type = self.type))
        print("Length: {length} bytes".format(length = self.length))

    def print_all(self):
        pass

    def ihdr_analyse(self):
        if self.length != 13:
            print("IHDR chunk's length is invalid")
        else:
            print("-"*10)
            print("Type: {type}".format(type = self.type))
            print("Width: {data}".format(data = int.from_bytes(self.data[0:4], byteorder = 'big')))
            print("Height: {data}".format(data = int.from_bytes(self.data[4:8], byteorder = 'big')))
            print("Bit depth: {data}".format(data = int.from_bytes(self.data[8:9], byteorder = 'big')))
            print("Color type: {data}".format(data = int.from_bytes(self.data[9:10], byteorder = 'big')))
            print("Filter method: {data}".format(data = filter_method(int.from_bytes(self.data[10:11], byteorder = 'big'))))
            if int.from_bytes(self.data[11:12],byteorder = 'big') == 0:
                print("Interlace method: No interlace")
            else:
                print("Interlace method: Adam7 interlace")


def filter_method(argument):
    switcher = {
        0: "None",
        1: "Sub",
        2: "Up",
        3: "Average",
        4: "Paeth",
    }
    return switcher.get(argument, "Not found")
