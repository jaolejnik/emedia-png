from chunks import Chunk


chunk_types = [b"IHDR", b"PLTE", b"IDAT", b"IEND"]
found_chunks = []

file = open("png_files/smiley.png", "rb") # open file
byte_string = file.read() # read all of it's data bytes
file.close() # close file

for type in chunk_types: # for each type in a chunk type list
    index = byte_string.find(type) # find an index where this type occurs
    type = type.decode("utf-8") # decode this type to pure string
    if type == "IEND": # if it's IEND chunk that marks end of the data
        length = 0
        data = None
        index += 4
        crc = byte_string[index:index+4].hex() # get it's CRC
    else:
        # get the length of the chunk's data in bytes, remove unnecesary ones,
        # transform to hex, then change it to int
        length = int(byte_string[index-4:index].replace(b"\x00", b"").hex(), 16)
        index += 4
        data = byte_string[index:index+length] # get chunk's data (in bytes for now)
        index += length
        crc = byte_string[index:index+4].hex() # get chunk's CRC (in hex for now)
    found_chunks.append(Chunk(length, type, data, crc))

for chunk in found_chunks:
    chunk.print_info()
