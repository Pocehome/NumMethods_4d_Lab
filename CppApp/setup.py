from setuptools import setup, Extension
import pybind11

pybind11_include = pybind11.get_include()

ext_modules = [
    Extension(
        'Lab_Spline_Module',
        ['TaskModule.cpp', 'Solver.cpp', 'Functions.cpp', 'Problems.cpp', 'Spline.cpp', 'tridiagonal_matrix_algorithm.cpp'],
        include_dirs=[pybind11_include],
        extra_compile_args=['/std:c++17'],
        extra_link_args=[],
    ),
]

setup(
    name='Lab_Spline_Module',
    version='1.0',
    ext_modules=ext_modules,
    zip_safe=False,
)
