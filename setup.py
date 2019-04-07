#!/usr/bin/env python
from __future__ import print_function
import os
from setuptools import setup

cur_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(cur_dir, 'README.rst')) as buf:
    README = buf.read()
with open(os.path.join(cur_dir, 'HISTORY.rst')) as buf:
    HISTORY = buf.read()


def build_native(spec):
    # build regex-capi ( RuRE )
    build = spec.add_external_build(
        cmd=['cargo', 'build', '--release'],
        path='./regex/regex-capi'
    )

    spec.add_cffi_module(
        module_path='rure._native',
        dylib=lambda: build.find_dylib('rure',
                                       in_path='../../regex/target/release'),
        header_filename=lambda: build.find_header('rure.h',
                                                  in_path='include'),
        rtld_flags=['NOW', 'NODELETE']
    )


setup(
    name='rure',
    version='0.2.1',
    author='David Blewett',
    author_email='david@dawninglight.net',
    description=('Python bindings for the Rust `regex` crate. '
                 'This implementation uses finite automata and guarantees '
                 'linear time matching on all inputs.'),
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    keywords=['regex', 'rust', 'dfa', 'automata', 'data_structures'],
    url='https://github.com/davidblewett/rure-python',
    setup_requires=['milksnake'],
    install_requires=['milksnake', 'cffi>=1.5.0', 'six'],
    milksnake_tasks=[
        build_native
    ],
    packages=['rure', 'rure.tests'],
    package_dir={'rure': 'rure'},
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Text Processing :: Indexing']
)
