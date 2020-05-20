from menu import Menu
from data import FilePNG
from rsa import RSA

file = FilePNG("../png_files/duze.png")
data = file.chunks['IDAT'].reconstructed_data
file.chunks['IDAT'].display_data("Primary")

key_size = 32

step = key_size // 8 - 1
data = [data[i:i+step] for i in range(0, len(data), step)]
data = [bytearray(slice) for slice in data]
data_sizes = [int.from_bytes(slice, 'big') for slice in data]
print(max(data_sizes))


rsa = RSA(max(data_sizes), key_size)
file.chunks['IDAT'].reconstructed_data = rsa.encryption(file.chunks['IDAT'].reconstructed_data)
file.chunks['IDAT'].display_data("Primary")
file.chunks['IDAT'].reconstructed_data = rsa.decryption(file.chunks['IDAT'].reconstructed_data)
file.chunks['IDAT'].display_data("Primary")
# file.print_to_file()
