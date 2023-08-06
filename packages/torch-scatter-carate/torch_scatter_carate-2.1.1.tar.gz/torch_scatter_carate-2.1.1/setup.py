import glob
import os
import os.path as osp
import platform
import sys
from itertools import product


from setuptools import find_packages, setup


__version__ = "2.1.1"
URL = "https://github.com/rusty1s/pytorch_scatter"


BUILD_DOCS = os.getenv("BUILD_DOCS", "0") == "1"
WITH_SYMBOLS = os.getenv("WITH_SYMBOLS", "0") == "1"

install_requires = ["torch"]

test_requires = [
    "pytest",
    "pytest-cov",
]


setup(
    name="torch_scatter_carate",
    version=__version__,
    description="PyTorch Extension Library of Optimized Scatter Operations adapted for compatibility",
    author="Matthias Fey",
    author_email="julian.kleber@sail.black",
    url=URL,
    download_url=f"{URL}/archive/{__version__}.tar.gz",
    keywords=["pytorch", "scatter", "segment", "gather"],
    python_requires=">=3.7",
    install_requires=install_requires,
    extras_require={
        "test": test_requires,
    },
    ext_modules=[],
    packages=find_packages(),
)
