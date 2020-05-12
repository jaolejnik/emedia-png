from chunks import Chunk
from const import DISPLAY_W


class TRNS(Chunk):
    '''
    Represents a tRNS ancillary chunk. Derivative of Chunk class.

    Fields:
        - transparency_data
    '''
    def __init__(self, raw_bytes, color_type, bit_depth):
        super().__init__(raw_bytes)
        self.organise_data(color_type)

    @staticmethod
    def bytes_per_pixel(color_type):
        '''
        Returns an amount of bytes ber pixel for given color_type.
        '''
        switcher = {
            0: 2,
            2: 6,
            3: 1,
        }
        return switcher[color_type]

    def organise_data(self, color_type):
        '''
        Gets slices of bytes with a proper size from self.data field, which
        contains raw bytes. Then it translates those slices from bytes to int.
        '''
        self.transparency_data = [self.data[i:i+TRNS.bytes_per_pixel(color_type)] for i in range(0, len(self.data), TRNS.bytes_per_pixel(color_type))]
        self.transparency_data = [int.from_bytes(pixel, "big") for pixel in self.transparency_data]

    def details(self):
        '''
        Prints chunk's details into stdout.
        '''
        self.basic_info()
        print("> TRANSPARENT PIXELS:\n  [ ID: VALUE ]\n  ------------")
        for i,pixel in enumerate(self.transparency_data, 1):
            if pixel != 255: print("  * {id}: {value}".format(id=i, value=pixel))
        print()


class TEXT(Chunk):
    '''
    Represents a tEXt ancillary chunk. Derivative of Chunk class.

    Fields:
        - transparency_data
    '''
    def __init__(self, init_data):
        if type(init_data) == list:
            super().__init__(uninit_chunk_list=init_data)
        else:
            super().__init__(raw_bytes=init_data)
        self.data_to_str()

    def data_to_str(self):
        '''
        Transforms raw bytes to strings.
        Gets slices of raw bytes, then splits each by NULL value to get keyword
        and value. Then transforms it to a formatted string.
        '''
        def decode_f(x):
            return x.decode("utf-8")
        self.data = [instance.split(b"\x00") for instance in self.data]
        self.data = [list(map(decode_f, instance_split)) for instance_split in self.data]
        for instance in self.data:
            instance[0] = instance[0].upper()

    def details(self):
        '''
        Prints chunk's details into stdout.
        '''
        self.basic_info()
        print(" ", end="")
        print(" tEXt DATA ".center(DISPLAY_W-2, "-"))
        for instance in self.data:
            print("> {keyword}: {content}".format(keyword=instance[0], content=instance[1]))
        print()


class GAMA(Chunk):
    '''
    gAma chunk specifies relationship between the image samples and the disared
    display output intensity as a power function.
    '''
    def __init__(self, raw_bytes):
        super().__init__(raw_bytes)
        self.analyse()

    def analyse(self):
        '''
        Gamma value is 4-bytes integer that represents gamma times 100000.
        '''
        self.gamma_value = int.from_bytes(self.data, "big")

    def details(self):
        print(" gAMA DATA ".center(DISPLAY_W-2, "-"))
        print(">Gamma Value: {value}\n".format(value = self.gamma_value))


class CHRM(Chunk):
    '''
    cHRM Chunk specify x,y chromaticities of red, green and blue primaries used
    in the image and the referenced white points.
    '''
    def __init__(self, raw_bytes):
        super().__init__(raw_bytes)
        self.analyse()

    def analyse(self):
        '''
        Each of these parametres is written in 4 bytes.
        '''
        self.chrm_values = { "white_point_x" : None,
                             "white_point_y" : None,
                             "red_x" : None,
                             "red_y" : None,
                             "green_x" : None,
                             "green_y" : None,
                             "blue_x" : None,
                             "blue_y" : None
                             }

        i = 0
        for chrm_key in self.chrm_values.keys():
            self.chrm_values[chrm_key] = int.from_bytes(self.data[i:i+4], "big")
            i += 4

    def details(self):
        print(" cHRM DATA ".center(DISPLAY_W-2, "-"))
        for chrm_part in self.chrm_values.keys():
            print("> {key}: {value}".format(key = chrm_part, value = self.chrm_values[chrm_part]))
        print()


class SRGB(Chunk):
    '''
    sRGB chunk contains 1-byte integer that is specified for the rendering
    intent defined by ICC. If this chunk is present, then image samples conform
    to sRGB color space.
    '''
    def __init__(self, raw_bytes):
        super().__init__(raw_bytes)
        self.analyse()

    @staticmethod
    def rendering_intent(int_data):
        switcher = {
            0: "Perceptual",
            1: "Relative colorimetric",
            2: "Saturation",
            3: "Absolute colorimetric"
        }
        return switcher.get(int_data, "Rendering intent not found")

    def analyse(self):

        self.rendering_intent = SRGB.rendering_intent(int.from_bytes(self.data, "big"))

    def details(self):
        print(" sRGB DATA ".center(DISPLAY_W-2, "-"))
        print("> RENDERING INTENT: ", self.rendering_intent)
        print()


class TIME(Chunk):
    '''
    The tIme Chunk gives the time of the last modification image in format
    Year-Month-Day | Hour-Minute-Second
    '''
    def __init__(self, raw_bytes):
        super().__init__(raw_bytes)
        self.analyse()

    def analyse(self):
        '''
        Year is written in 2 bytes and
        the other parts of the time in 1 byte
        '''
        self.time_parts = {
        "Year" : None,
        "Month" : None,
        "Day" : None,
        "Hour" : None,
        "Minute" : None,
        "Second" : None
        }

        i = 2
        for time_key in self.time_parts.keys():
            if time_key == "Year":
                self.time_parts["Year"] = int.from_bytes(self.data[0:2], "big")
            else:
                self.time_parts[time_key] = int.from_bytes(self.data[i:i+1], "big")
                i += 1

    def details(self):
        print(" tIME DATA ".center(DISPLAY_W-2, "-"))
        for time_key in self.time_parts.keys():
            print("> {key}: {value}".format(key = time_key, value = self.time_parts[time_key]))
        print()
