from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.8'
DESCRIPTION = 'Ultra high-level Python library for processing and analysing geo-data.'
LONG_DESCRIPTION = 'This library further abstracts Python libraries such as Pandas, Matplotlib, and Numpy so that non-developers can use Python to process and analyse GNSS data, telemetry data, and other spatial-temporal data. May it enlighten users with understanding, like the goddess Gayatri - on mother earth (Gaia) and beyond..'

# Setting up
setup(
    name="Gaiatri",
    version=VERSION,
    author="MotherBunker (A.N.A. Martam)",
    author_email="<motherrrcorp@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas','matplotlib','numpy'],
    keywords=['python','geospatial','geographical information systems','telemetry'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)