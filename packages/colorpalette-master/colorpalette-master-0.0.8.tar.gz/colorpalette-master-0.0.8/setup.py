from setuptools import setup, find_packages
import codecs
import os

setup(
    name = "colorpalette-master",
    version = "0.0.8",
    author = "Victor Andrievskiy",
    author_email = "superavb222@gmail.com",
    description= "Scripts for generating a color palette out of an image",
    long_description= "Scripts for generating a color palette out of an image, based on median cut algorithm. Used in my college project PixPalette.",
    packages=find_packages(),
    install_requires = ['scikit-image', 'numpy', 'Pillow==9.4.0', 'image-decoding-algorithms'],
    url = "https://github.com/gejirz/colorpalette-master",
    keywords=['python', 'color palette', 'median cut quantization', 'PixPalette', 'median cut'],
    license= "MIT License"
)