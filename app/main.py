from menu import Menu
from data import FilePNG
from own_rsa import RSA

file = FilePNG("../png_files/ship.png")
data = file.chunks['IDAT'].reconstructed_data
# file.chunks['IDAT'].display_data("Primary")
key_size = 32

file = FilePNG("../png_files/dice.png")
data = file.chunks['IDAT'].reconstructed_data
file.chunks['IDAT'].display_data("ORYGINAŁ")

key_size = 1024


step = key_size // 8 - 1
data = [data[i:i+step] for i in range(0, len(data), step)]
data = [bytearray(slice) for slice in data]
data_sizes = [int.from_bytes(slice, 'big') for slice in data]
print(max(data_sizes))


rsa = RSA(max(data_sizes), key_size)

# print(rsa.check_if_encryption_correct(file.chunks['IDAT'].reconstructed_data))
# print(type(file.chunks['IDAT'].compressed_data))
# file.chunks['IDAT'].reconstructed_data = rsa.encryption(file.chunks['IDAT'].compressed_data)
# file.chunks['IDAT'].display_data("Primary")
# file.chunks['IDAT'].reconstructed_data = rsa.decryption(file.chunks['IDAT'].decompressed_data)
# file.chunks['IDAT'].display_data("Primary")

file.chunks['IDAT'].reconstructed_data = rsa.encryption_cbc(file.chunks['IDAT'].reconstructed_data)
file.chunks['IDAT'].display_data("ZASZYFROWANE", data=[float(x) for x in file.chunks['IDAT'].reconstructed_data])
file.chunks['IDAT'].reconstructed_data = rsa.decryption_cbc(file.chunks['IDAT'].reconstructed_data)
file.chunks['IDAT'].display_data("ROZSZYFROWANE")

# file.print_to_file()

# file.chunks['IDAT'].reconstructed_data = rsa.encrypt_with_ready_solution(file.chunks['IDAT'].reconstructed_data)
# file.chunks['IDAT'].display_data("Primary")
# file.chunks['IDAT'].reconstructed_data = rsa.decrypt_with_ready_solution(file.chunks['IDAT'].reconstructed_data)
# file.chunks['IDAT'].display_data("Primary")