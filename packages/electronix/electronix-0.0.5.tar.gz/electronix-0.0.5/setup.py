from setuptools import setup, find_packages
import codecs
import os

VERSION = "0.0.5"
DESCRIPTION = "A basic and simple package for learning about electronics and computer science"
LONG_DESCRIPTION = "A basic and simple package for learning about electronics and computer science and expreimenting using Python programming language"

# Setting up
setup(
    name="electronix",
    version=VERSION,
    author="VelikiFeniks",
    author_email="veliki.feniks@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=["python", "electronics", "computer science", "logic gates", "binary", "ASCII", "octal", "hex"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)