from chunks import Chunk
from ihdr import IHDR
from plte import PLTE
from parse_data import parse_data


file = open("png_files/smiley.png", "rb") # open file
byte_string = file.read() # read all of it's data bytes
file.close() # close file

length, data, crc = parse_data(byte_string, b"IHDR")
test_IHDR = IHDR(length, data, crc)
test_IHDR.print_info()

length, data, crc = parse_data(byte_string, b"PLTE")
test_PLTE = PLTE(length, data, crc, test_IHDR.color_type)
test_PLTE.print_info()
test_PLTE.print_palette()
