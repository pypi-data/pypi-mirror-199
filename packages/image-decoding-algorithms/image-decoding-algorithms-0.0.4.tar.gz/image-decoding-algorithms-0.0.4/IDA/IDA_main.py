from sys import path, version_info
from pathlib import Path
path.append(str(Path(__file__).parent.resolve()))
from JFIFDecoder import decode as JFIF_decoder
from Image_reader import Image_reading_class as Image_reader

from numpy import asarray, ndarray
from skimage.io import imread

JFIF_FILE_TEST_SIZE = 11
def read_image(path: str) -> ndarray:
    py_ver = True
    if not (version_info.major == 3 and version_info.minor == 7 and version_info.micro == 7):
        py_ver = False
    read_not_failed = True
    raw_img = list
    img = ndarray

    image = Image_reader(path)
    file_test = image.read_str(JFIF_FILE_TEST_SIZE)
    if file_test.startswith(b'\xff\xd8\xff\xe0') and file_test.endswith(b'JFIF\x00'): #signature of JFIF format
        image.read(file_test[5] - JFIF_FILE_TEST_SIZE)
        try:
            raw_img = JFIF_decoder(image)
        except:
            read_not_failed = False
    else:
        read_not_failed = False

    if read_not_failed and py_ver:
        img = asarray(raw_img)
    else:
        img = imread(path)

    return img
