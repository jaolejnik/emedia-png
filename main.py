from data import FilePNG


# pathname = input()
pathname = "png_files/pokemon.png"
png_file = FilePNG(pathname)
png_file.print_info()
png_file.print_chunks()
