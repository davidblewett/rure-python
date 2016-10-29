import os
from setuptools import setup

from rust_setuptools import (build_rust_cmdclass, build_install_lib_cmdclass,
                             RustDistribution)
#from rust_setuptools import RustDistribution, install_lib_cmdclass

cur_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(cur_dir, 'README.rst')) as buf:
    README = buf.read()

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
        'cffi>=1.7.0'],
    install_requires=['cffi>=1.7.0'],
    cffi_modules=['rure/_build_ffi.py:ffi'],
    distclass=RustDistribution,
    cmdclass={
        'build_rust': build_rust_cmdclass([(cur_dir, 'rure')]),
        'install_lib': build_install_lib_cmdclass()
        #'install_lib': install_lib_cmdclass()
    },
    packages=['rure'],
    package_dir={'rure': 'rure'},
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Text Processing :: Indexing']
)
