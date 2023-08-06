from sys import path
from pathlib import Path
path.append(str(Path(__file__).parent.resolve()))
from JFIFDecoder import decode as JFIF_decoder
from Image_reader import Image_reading_class as Image_reader

from numpy import asarray, ndarray
from skimage.io import imread

JFIF_FILE_TEST_SIZE = 11
def read_image(path: str) -> ndarray:
    read_failed = False
    raw_img = list
    img = ndarray

    image = Image_reader(path)
    file_test = image.read_str(JFIF_FILE_TEST_SIZE)
    if file_test.startswith(b'\xff\xd8\xff\xe0') and file_test.endswith(b'JFIF\x00'): #signature of JFIF format
        image.read(file_test[5] - JFIF_FILE_TEST_SIZE)
        print("That`s a JFIF FILE!")
        try:
            raw_img = JFIF_decoder(image)
        except:
            read_failed = True
    else:
        read_failed = True

    if read_failed:
        img = imread(path)
    else:
        img = asarray(raw_img)

    return img
