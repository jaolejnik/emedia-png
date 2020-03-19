from chunks import Chunk
from ihdr import IHDR
from plte import PLTE
from data import *


# pathname = input()
pathname = "png_files/duze.png"
name, size, byte_string = load_data(pathname)
file_info(name, size)

length, data, crc = parse_data(byte_string, b"IHDR")
chunk_IHDR = IHDR(length, data, crc)
chunk_IHDR.print_info()
