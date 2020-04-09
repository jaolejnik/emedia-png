from chunks import Chunk
from const import DISPLAY_W

def bytes_per_pixel(color_type):
    switcher = {
        0: 2,
        2: 6,
        3: 1,
    }
    return switcher[color_type]

def rendering_intent(argument):
    switcher = {
        0: "Perceptual",
        1: "Relative colorimetric",
        2: "Saturation",
        3: "Absolute colorimetric"
    }
    return switcher.get(argument, "Rendering intent not found")

class TRNS(Chunk):
    def __init__(self, raw_bytes, color_type, bit_depth):
        super().__init__(raw_bytes)
        self.organise_data(color_type)

    def organise_data(self, color_type):
        self.transparency_data = [self.data[i:i+bytes_per_pixel(color_type)] for i in range(0, len(self.data), bytes_per_pixel(color_type))]
        self.transparency_data = [int.from_bytes(pixel, "big") for pixel in self.transparency_data]

    def details(self):
        self.basic_info()
        print("> TRANSPARENT PIXELS:\n  [ ID: VALUE ]\n  ------------")
        for i,pixel in enumerate(self.transparency_data, 1):
            if pixel != 255: print("  * {id}: {value}".format(id=i, value=pixel))
        print()


class TEXT(Chunk):
    def __init__(self, init_data):
        if type(init_data) == list:
            super().__init__(uninit_chunk_list=init_data)
        else:
            super().__init__(raw_bytes=init_data)
        self.data_to_str()

    def data_to_str(self):
        def decode_f(x):
            return x.decode("utf-8")
        self.data = [instance.split(b"\x00") for instance in self.data]
        self.data = [list(map(decode_f, instance_split)) for instance_split in self.data]
        for instance in self.data:
            instance[0] = instance[0].upper()

    def details(self):
        self.basic_info()
        print(" ", end="")
        print(" tEXt DATA ".center(DISPLAY_W-2, "-"))
        for instance in self.data:
            print("> {keyword}: {content}".format(keyword=instance[0], content=instance[1]))
        print()


class GAMA(Chunk):
    def __init__(self, raw_bytes):
        super().__init__(raw_bytes)
        self.analyse()

    def analyse(self):
        self.gamma_value = int.from_bytes(self.data, "big")

    def details(self):
        print(" gAMA DATA ".center(DISPLAY_W-2, "-"))
        print(">Gamma Value: {value}\n".format(value = self.gamma_value))


class CHRM(Chunk):
    def __init__(self, raw_bytes):
        super().__init__(raw_bytes)
        self.analyse()

    def analyse(self):
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
    def __init__(self, raw_bytes):
        super().__init__(raw_bytes)
        self.analyse()

    def analyse(self):
        self.rendering_intent = rendering_intent(int.from_bytes(self.data, "big"))

    def details(self):
        print(" sRGB DATA ".center(DISPLAY_W-2, "-"))
        print(">Rendering intent: {value}".format(value = self.rendering_intent))
        print()


class TIME(Chunk):
    def __init__(self, raw_bytes):
        super().__init__(raw_bytes)
        self.analyse()

    def analyse(self):
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
