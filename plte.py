from chunks import Chunk

class Plte(Chunk):
    def __init__(self, green, red, blue, length, data):
        super().__init__(length,data)
        self.green = green
        self.red = red
        self.blue = blue

    def print_info(self):
        print("Red: {self.red}\n Green: {self.green}\n Blue: {self.blue}")
