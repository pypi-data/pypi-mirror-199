from setuptools import setup, find_packages
import codecs
import os

setup(
    name = "image-decoding-algorithms",
    version = "0.0.1",
    author = "Victor Andrievskiy",
    author_email = "superavb222@gmail.com",
    description= "Scripts for decoding an image",
    long_description= "Scripts for decoding an image. Myself have written a decoding algorithm for JFIF, baseline encoding mode, used skimage for everything else.",
    packages=find_packages(),
    install_requires = ['scikit-image', 'numpy'],
    url = "https://github.com/gejirz/image-decoding-algorithms",
    keywords=['python', 'image decoding', 'JFIF', 'jpeg', 'decoding', 'baseline encoding'],
    license= "MIT License"
)