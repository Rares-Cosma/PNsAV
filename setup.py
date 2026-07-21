import sys
import pybind11
from setuptools import setup, Extension

# Detect the OS and set the correct C++17 flag
if sys.platform == "win32":
    cpp_flags = ['/std:c++17', '/O2']  # Windows/MSVC
else:
    cpp_flags = ['-std=c++17', '-O3']  # Linux/GCC (Streamlit Cloud)

ext = Extension(
    'ArgEngine', 
    sources=[
        'PNsAV/src/core/engine/bindings.cpp',
        'PNsAV/src/core/engine/engine.cpp',
        'PNsAV/src/core/engine/symbolic_utils.cpp'
    ],
    include_dirs=[
        pybind11.get_include(),
        'PNsAV/src/core/engine'
    ],
    extra_compile_args=cpp_flags, # <--- We added the compiler flags here
    language='c++'
)

setup(
    name='ArgEngine',
    ext_modules=[ext],
)