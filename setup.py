#!/usr/bin/env python
from __future__ import print_function
import os
from setuptools import setup

from rust_setuptools import (build_rust_cmdclass, build_install_lib_cmdclass,
                             RustDistribution)
#from rust_setuptools import RustDistribution, install_lib_cmdclass

cur_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(cur_dir, 'README.rst')) as buf:
    README = buf.read()
rure_dir = os.getenv('RURE_DIR', cur_dir)
print('rure_dir:', rure_dir)

setup(
    name='rure',
    version='0.1.1',
    author='David Blewett',
    author_email='david@dawninglight.net',
    description=('Python bindings for the Rust `regex` create. '
                 'This implementation uses finite automata and guarantees '
                 'linear time matching on all inputs.'),
    long_description=README,
    license='MIT',
    keywords=['regex', 'rust', 'dfa', 'automata', 'data_structures'],
    url='https://github.com/davidblewett/rure-python',
    setup_requires=[
        'cffi>=1.5.0'],
    install_requires=['cffi>=1.5.0'],
    cffi_modules=['rure/_build_ffi.py:ffi'],
    distclass=RustDistribution,
    cmdclass={
        'build_rust': build_rust_cmdclass([(rure_dir, 'rure')]),
        'install_lib': build_install_lib_cmdclass()
        #'install_lib': install_lib_cmdclass()
    },
    packages=['rure', 'rure.tests'],
    package_dir={'rure': 'rure'},
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Text Processing :: Indexing']
)
