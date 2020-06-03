import re
from glob import glob
from os import system
from matplotlib import pyplot as plt
from data import FilePNG
from rsa import RSA

class Menu:
    '''
    Represents simple menu made with C-like switch cases.
    '''
    def __init__(self):
        self.choice = None
        self.active_menu = self.main_menu
        self.active_options = self.main_options
        self.rsa = None

    def set_file_list(self, dir_path):
        '''
        Gets list of defualt files that are store in png_files dir.
        '''
        self.defualt_files = glob(dir_path+"*.png")

    def start(self):
        '''
        Statrs the loop that's responsible for keeping the program running and
        input handling.
        '''
        system("clear")
        plt.ion()
        plt.show()
        self.set_file_list("../png_files/")
        while self.choice != 'q' or self.choice != 'Q':
            self.active_options()
            self.active_menu()


    def main_options(self):
        '''
        Displays possible options for the main menu.
        '''
        print("WHAT DO YOU WANT TO DO NEXT?\n")
        for i,file in enumerate(self.defualt_files, 1):
            name = re.findall('\w+.png', file)[0]
            print(" [{}] - {}".format(i, name[:-4]))
        print()
        print(" [F] - Load a custom PNG file.")
        print()
        print(" [Q] - Quit\n")


    @staticmethod
    def file_options():
        '''
        Displays possible options for the file menu.
        '''
        print("WHAT DO YOU WANT TO DO NEXT?\n")
        print(" [1] - Print file's basic info.")
        print(" [2] - Print file's chunks.")
        print(" [3] - Go to chunks menu (for more details).")
        print(" [4] - Save as a new file with only critical chunks.")
        print(" [5] - Perform FFT.")
        print(" [6] - Cryptography")
        print()
        print(" [B] - Go back.")
        print(" [Q] - Quit\n")

    @staticmethod
    def crypt_options():
        '''
        Displays possible options for the crypt menu.
        '''
        print("WHAT DO YOU WANT TO DO NEXT?\n")
        print(" [1] - Encrypt (selfmade, EBC)")
        print(" [2] - Decrypt (selfmade, EBC)")
        print()
        print(" [3] - Encrypt (selfmade, CBC)")
        print(" [4] - Decrypt (selfmade, CBC)")
        print()
        print(" [B] - Go back.")
        print(" [Q] - Quit\n")

    def chunks_options(self):
        '''
        Displays possible options for the chunks menu.
        '''
        print("WHAT DO YOU WANT TO DO NEXT?\n")
        for i,chunk in enumerate(self.original_file.chunks.keys(), 1):
            print(" [{}] - {} details.".format(i, chunk))
        print()
        if "PLTE" in self.original_file.chunks.keys():
            print(" [P] - Apply the color palette on IDAT's data.")
        if "tRNS" in self.original_file.chunks.keys():
            print(" [T] - Apply transparency on IDAT's data.")
        print()
        print(" [B] - Go back.")
        print(" [Q] - Quit\n")


    @staticmethod
    def invalid_option(*args):
        '''
        *args is there only if choice in a menu needs to be called with an
        argument.
        '''
        print("Invalid option! Try again.")


    def load_file(self, pathname=None):
        '''
        Loads the file with the given pathname.
        '''
        if pathname == None:
            self.pathname = input(" Enter PNG file's pathname:\n  >>")
        else: self.pathname = pathname
        self.original_file = FilePNG(self.pathname)
        system("clear")
        print("> LOADED FILE: {}.png".format(self.original_file.name))
        print()


    def main_menu(self):
        '''
        Handles choice for the main menu.
        '''
        def file_loading(choice):
            if choice == 'f': self.load_file()
            else: self.load_file(self.defualt_files[int(choice)-1])
            self.active_menu = self.file_menu
            self.active_options = Menu.file_options

        switch = {
        'f': file_loading,
        'q': exit,
        }
        for i,file in enumerate(self.defualt_files, 1):
            switch[str(i)] = file_loading
        choice = input(">> ").lower()
        system("clear")
        switch.get(choice, Menu.invalid_option)(choice)


    def file_menu(self):
        '''
        Handles choice for the file menu.
        '''
        assert self.original_file != None, "A file should be loaded first!"

        def go_back():
            self.original_file = None
            self.active_menu = self.main_menu
            self.active_options = self.main_options

        def switch_chunks_menu():
            self.active_menu = self.chunks_menu
            self.active_options = self.chunks_options

        def switch_crypt_menu():
            self.active_menu = self.crypt_menu
            self.active_options = self.crypt_options

        switch = {
        '1': self.original_file.print_info,
        '2': self.original_file.print_chunks,
        '3': switch_chunks_menu,
        '4': self.original_file.print_to_file,
        '5': self.original_file.perform_fft,
        '6': switch_crypt_menu,
        'b': go_back,
        'q': exit,
        }
        choice = input(">> ").lower()
        system("clear")
        switch.get(choice, Menu.invalid_option)()


    def chunks_menu(self):
        '''
        Handles choice for the chunks menu.
        '''
        def go_back():
            self.active_menu = self.file_menu
            self.active_options = Menu.file_options

        def palette_application():
            self.original_file.chunks["IDAT"].apply_palette(self.original_file.chunks["PLTE"].palettes)

        def transparency_application():
            if "PLTE" in self.original_file.chunks.keys():
                self.original_file.chunks["IDAT"].apply_transparency(self.original_file.chunks["tRNS"].transparency_data,
                                                                     palette=self.original_file.chunks["PLTE"].palettes)
            else:
                self.original_file.chunks["IDAT"].apply_transparency(self.original_file.chunks["tRNS"].transparency_data)

        switch = {
        'b': go_back,
        'q': exit,
        }
        for i,chunk in enumerate(self.original_file.chunks.values(), 1):
            switch[str(i)] = chunk.details
        if "PLTE" in self.original_file.chunks.keys():
            switch['p'] = palette_application
        if "tRNS" in self.original_file.chunks.keys():
            switch['t'] = transparency_application
        choice = input(">> ").lower()
        system("clear")
        switch.get(choice, Menu.invalid_option)()

    def crypt_menu(self):
        encrypted_data = None
        decrypted_data = None

        def encrypt():
            global encrypted_data
            system("clear")
            print("Specify key size:")
            key_size = int(input(">> ").lower())
            data = self.original_file.chunks['IDAT'].reconstructed_data
            step = key_size // 8 - 1
            data = [data[i:i+step] for i in range(0, len(data), step)]
            data = [bytearray(slice) for slice in data]
            data_sizes = [int.from_bytes(slice, 'big') for slice in data]
            self.rsa = RSA(max(data_sizes), key_size)

            self.original_file.chunks['IDAT'].display_data("ORIGINAL")
            encrypted_data = self.rsa.encryption(self.original_file.chunks['IDAT'].reconstructed_data)
            self.original_file.chunks['IDAT'].display_data("ENCRYPTED", data=encrypted_data)

        def decrypt():
            global decrypted_data, encrypted_data
            decrypted_data = self.rsa.decryption(encrypted_data)
            self.original_file.chunks['IDAT'].display_data("DECRYPTED", data=decrypted_data)

        def encrypt_cbc():
            global encrypted_data
            system("clear")
            print("Specify key size:")
            key_size = int(input(">> ").lower())
            data = self.original_file.chunks['IDAT'].reconstructed_data
            step = key_size // 8 - 1
            data = [data[i:i+step] for i in range(0, len(data), step)]
            data = [bytearray(slice) for slice in data]
            data_sizes = [int.from_bytes(slice, 'big') for slice in data]
            self.rsa = RSA(max(data_sizes), key_size)

            self.original_file.chunks['IDAT'].display_data("ORIGINAL")
            encrypted_data = self.rsa.encryption_cbc(self.original_file.chunks['IDAT'].reconstructed_data)
            self.original_file.chunks['IDAT'].display_data("ENCRYPTED CBC", data=[float(x) for x in encrypted_data])

        def decrypt_cbc():
            global decrypted_data, encrypted_data
            decrypted_data = self.rsa.decryption_cbc(encrypted_data)
            self.original_file.chunks['IDAT'].display_data("DECRYPTED CBC", data=decrypted_data)

        def go_back():
            self.active_menu = self.file_menu
            self.active_options = Menu.file_options


        switch = {
        '1': encrypt,
        '2': decrypt,
        '3': encrypt_cbc,
        '4': decrypt_cbc,
        'b': go_back,
        'q': exit,
        }
        choice = input(">> ").lower()
        system("clear")
        switch.get(choice, Menu.invalid_option)()
