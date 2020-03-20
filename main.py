from data import FilePNG


# pathname = input()
pathname = "png_files/smiley.png"
png_file = FilePNG("png_files/smiley.png")
png_file.print_info()
png_file.print_chunks()
