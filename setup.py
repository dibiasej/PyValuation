# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname('/Users/debos/Downloads/PyValuation/'))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="PyValuation",
    version="0.1.0",
    description="Demo library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://PyValuation.readthedocs.io/",
    author="Jason DiBiase",
    author_email="dibiasej3@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["PyValuation"],
    include_package_data=True,
    install_requires=["numpy", "yfinance", "pandas", "bs4", "requests", "numpy_financial", "matplotlib.pyplot", "seaborn", "pandas_datareader", "datetime",
                     "os", "scipy.optimize", "scipy.interpolate", "plotly.express", "plotly.graph_objects", "plotly.subplots"]
)