# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="tweets_preprocess",
    version="0.1.0",
    description="Library for tweets preprocessing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://tweets_preprocess.readthedocs.io/",
    author="Anusha Kotha",
    author_email="anusha.kotha@indianpac.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["tweets_preprocess"],
    include_package_data=True,
    install_requires=["numpy","pandas","regex","re"]
)