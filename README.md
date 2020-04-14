# emedia-png
Project for an university course about processing electronic media files. \
The goal was to create a simple program to parse a **PNG** file byte by byte and get the information stored in file's chunks.

## Functionality
- Look up file's chunks and their details.
- Recreate an image from raw IDAT's data and apply chunk of your choice.
- Save as a new PNG file with only critical chunks.
- Perform the Fourier Transform.

## Supported chunks
### Critical chunks
- IHDR
- IDAT
- PLTE
- IEND
### Ancillary chunks
- tRNS
- gAMA
- cHRM
- sRGB
- tEXt
- tIME \
... and more to come (*or maybe not*).

## Dependencies
- Python 3.6 or higher
- [NumPy](https://numpy.org/)
- [Matplotlib](https://matplotlib.org/)
- [OpenCV](https://opencv-python-tutroals.readthedocs.io/en/latest/index.html)
