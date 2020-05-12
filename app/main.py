from menu import Menu
from data import FilePNG
from rsa import RSA

file = FilePNG("/home/vimmor/MyDocuments/emedia-png/png_files/linux.png")
rsa = RSA()
file.chunks['IDAT'].display_data("Primary")
file.chunks['IDAT'].reconstructed_data = rsa.encryption(file.chunks['IDAT'])
# file.chunks['IDAT'].display_data("Primary")
file.chunks['IDAT'].reconstructed_data = rsa.decryption(file.chunks['IDAT'].reconstructed_data)
file.chunks['IDAT'].display_data("Primary")
# file.print_to_file()
