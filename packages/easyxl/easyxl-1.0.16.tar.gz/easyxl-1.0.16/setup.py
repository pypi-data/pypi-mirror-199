import os
import codecs

from setuptools import setup, find_packages
# from importlib.util import module_from_spec, spec_from_file_location

# spec = spec_from_file_location("constants", "./easyxlwings/_constants.py")
# constants = module_from_spec(spec)
# spec.loader.exec_module(constants)


here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, "README.md"), encoding='utf-8') as fh:
    long_description = "\\n" + fh.read()


__name__ = "easyxl"
__author__ = "leeheisen"
__license__ = "MIT License"
__url__= "https://github.com/leeheisen/easyxl"
__version__ = "1.0.16"

setup(
    name=__name__,
    version=__version__,
    author=__author__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=__url__,
    install_requires=['xlwings', 'json5', 'mjson5'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={},
    packages=find_packages(),
    python_requires=">=3.8",
)

