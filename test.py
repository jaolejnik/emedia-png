from chunks import Chunk
from ihdr import IHDR
from plte import PLTE
from data import *

# name, size, tmp = load_data("png_files/duze.png")
# file_info(name, size)

file = open("png_files/gradient.png", "rb") # open file
byte_string = file.read() # read all of it's data bytes
file.close() # close file

length, data, crc = parse_data(byte_string, b"IHDR")
test_IHDR = IHDR(length, data, crc)
test_IHDR.print_info()

if test_IHDR.color_type == 3:
    length, data, crc = parse_data(byte_string, b"PLTE")
    test_PLTE = PLTE(length, data, crc, test_IHDR.color_type)
    test_PLTE.print_info()
    test_PLTE.plot_palette()
    # test_PLTE.print_palette()
