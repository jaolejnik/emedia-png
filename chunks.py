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

    
