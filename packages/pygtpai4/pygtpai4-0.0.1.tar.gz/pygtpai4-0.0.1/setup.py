import os
from setuptools import setup, find_packages
pkg = os.path.abspath(os.path.dirname(__file__))
setup(
    name="pygtpai4",
    version="0.0.1",
    author="Noxi",
    author_email="ex@email.com",
    description = ("GTP - 4"),
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        ]
)