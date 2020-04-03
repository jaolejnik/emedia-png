from data import FilePNG
from os import system



class Menu:
    def __init__(self):
        self.choice = None
        self.active_menu = self.main_menu
        self.active_options = self.main_options


    def start(self):
        system("clear")
        while self.choice != 'q' or self.choice != 'Q':
            self.active_options()
            self.active_menu()


    @staticmethod
    def main_options():
        print("WHAT DO YOU WANT TO DO NEXT?\n")
        print(" [1] - Load PNG file.")
        print(" [Q] - Quit\n")


    @staticmethod
    def file_options():
        print("WHAT DO YOU WANT TO DO NEXT?\n")
        print(" [1] - Print file's basic info.")
        print(" [2] - Print file's chunks.")
        print(" [3] - Go to chunks menu (for more details).")
        print(" [B] - Go back.")
        print(" [Q] - Quit\n")


    def chunks_options(self):
        print("WHAT DO YOU WANT TO DO NEXT?\n")
        for i,chunk in enumerate(self.original_file.chunks.keys(), 1):
            print(" [{}] - {} details.".format(i, chunk))
        print(" [B] - Go back.")
        print(" [Q] - Quit\n")


    @staticmethod
    def invalid_option():
        print("Invalid option! Try again.")


    def load_file(self):
        # self.pathname = input(" Enter PNG file's pathname:\n  >>")
        self.pathname = "png_files/smiley.png"
        self.original_file = FilePNG(self.pathname)


    def main_menu(self):
        def load_file():
            self.load_file()
            self.active_menu = self.file_menu
            self.active_options = Menu.file_options

        switch = {
        '1': load_file,
        'q': exit,
        }
        choice = input(">> ").lower()
        system("clear")
        switch.get(choice, Menu.invalid_option)()


    def file_menu(self):
        assert self.original_file != None, "A file should be loaded first!"

        def go_back():
            self.original_file = None
            self.active_menu = self.main_menu
            self.active_options = Menu.main_options

        def chunks_menu():
            self.active_menu = self.chunks_menu
            self.active_options = self.chunks_options

        switch = {
        '1': self.original_file.print_info,
        '2': self.original_file.print_chunks,
        '3': chunks_menu,
        'b': go_back,
        'q': exit,
        }
        choice = input(">> ").lower()
        system("clear")
        switch.get(choice, Menu.invalid_option)()


    def chunks_menu(self):
        def go_back():
            self.active_menu = self.file_menu
            self.active_options = Menu.file_options

        switch = {
        'b': go_back,
        'q': exit,
        }
        for i,chunk in enumerate(self.original_file.chunks.values(), 1):
            switch[str(i)] = chunk.details
        choice = input(">> ").lower()
        system("clear")
        switch.get(choice, Menu.invalid_option)()
