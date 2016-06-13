#
# Setup.py file for Cython builder. Requires Cython code in a .pyx file.
# Build with this command ---> python setup.py build_ext --inplace
#

from distutils.core import setup
from Cython.Build import cythonize

filename = "helloworld.pyx"

setup(
    ext_modules = cythonize(filename)
)
