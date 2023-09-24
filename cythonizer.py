from setuptools import setup
from Cython.Build import cythonize

setup(
    packages=["rinha_interpreter"],
    ext_modules=cythonize([
        "./rinha_interpreter/core/environment.py",
        "./rinha_interpreter/core/evaluate.py",
    ], annotate=True),
)

# python3 cythonizer.py build_ext --inplace
