from const import DISPLAY_W

class Chunk:
    '''
    This class is responsible for representing a chunk in a PNG file.
    This is a base for every other class that is created for a particular type
    of a chunk.

    Fields:
        - length
        - type
        - data
        - crc
    '''
    def __init__(self, raw_bytes=None, uninit_chunk_list=None):
        '''
        I'm sure there is a better way to do this and this solution is terrible,
        but I'm on a tight deadline. - jaolejnik
        '''
        if raw_bytes and not uninit_chunk_list:
            self.single_chunk_init(raw_bytes)
        elif not raw_bytes and uninit_chunk_list:
            self.multiple_chunk_init(uninit_chunk_list)
        elif raw_bytes and uninit_chunk_list:
            raise Exception("Cannot pass raw_bytes AND uninit_chunk_list!")
        else:
            raise Exception("No argument given! Pass raw_bytes OR uninit_chunk_list!")

    def single_chunk_init(self, raw_bytes):
        '''
        Initialiazes an object with raw bytes of a single chunk as an input.
        '''
        i = 0
        self.length = int.from_bytes(raw_bytes[i:i+4], "big")
        i += 4
        self.type = raw_bytes[i:i+4].decode("utf-8")
        i += 4
        self.data = raw_bytes[i:i+self.length]
        i += self.length
        self.crc = raw_bytes[i:i+4]

    def multiple_chunk_init(self, uninit_chunk_list):
        '''
        Initialiazes an object with a data from a list of Chunk objects as an
        input. It's mian goal is to merge multiple instances of chunks of the
        same type into one.
        '''
        self.length = [chunk.length for chunk in uninit_chunk_list]
        self.type = uninit_chunk_list[0].type
        self.data = [chunk.data for chunk in uninit_chunk_list]
        self.crc = [chunk.crc for chunk in uninit_chunk_list]

    def basic_info(self):
        '''
        Print chunk's basic info.
        '''
        print(" {type} CHUNK ".format(type=self.type).center(DISPLAY_W, "="))
        print(" ", end="")
        print(" BASIC INFO ".center(DISPLAY_W-2, "-"))
        print("> TYPE:", self.type)
        print("> LENGTH: {length} bytes".format(length = self.length))
        print("> CRC: ", self.crc)
        print()

    def details(self):
        '''
        Print chunk's details into stdout (as it is a base class, non are defined).
        '''
        print("> None defined for this chunk (yet).")
        print()
