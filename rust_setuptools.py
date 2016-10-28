# -*- coding: utf-8 -*-
""" Based on code by Armin Ronacher, James Salter, Johannes Baiter

https://github.com/mitsuhiko/rust-setuptools
https://github.com/novocaine/rust-python-ext
https://github.com/jbaiter/python-rust-fst
"""
from __future__ import print_function

import os
import sys
import shutil
import subprocess

from distutils.cmd import Command
from distutils.command.install_lib import install_lib
from distutils.dist import Distribution


if sys.platform == 'win32':
    DYNAMIC_LIB_SUFFIX = '.dll'
elif sys.platform == 'darwin':
    DYNAMIC_LIB_SUFFIX = '.dylib'
else:
    DYNAMIC_LIB_SUFFIX = '.so'


class RustDistribution(Distribution):

    def __init__(self, attrs=None):
        Distribution.__init__(self, attrs)
        self.ext_modules = []

    def has_ext_modules(self):
        return True


class RustBuildCommand(Command):
    description = 'build rust crates into Python extensions'

    user_options = []

    def initialize_options(self):
        for k, v in self.__class__.rust_build_args.items():
            setattr(self, k, v)

    def finalize_options(self):
        pass

    def run(self):
        # Force binary wheel
        self.distribution.has_ext_modules = lambda: True
        self.distribution.ext_modules = []

        # Make sure that if pythonXX-sys is used, it builds against the
        # current executing python interpreter.
        bindir = os.path.dirname(sys.executable)
        if sys.platform == 'win32':
            path_sep = ';'
        else:
            path_sep = ':'

        env = dict(os.environ)
        env.update({
            # disables rust's pkg-config seeking for specified packages,
            # which causes pythonXX-sys to fall back to detecting the
            # interpreter from the path.
            'PYTHON_2.7_NO_PKG_CONFIG': '1',
            'PATH':  bindir + path_sep + env.get('PATH', '')
        })

        for crate_path, dest in self.cargo_crates:
            # Find the shared library that cargo hopefully produced and copy
            # it into the build directory as if it were produced by
            # build_cext.
            if self.debug:
                suffix = 'debug'
            else:
                suffix = 'release'

            dylib_path = os.path.join(crate_path, 'target/', suffix)

            # Ask build_ext where the shared library would go if it had built it,
            # then copy it there.
            build_ext = self.get_finalized_command('build_ext')

            target = os.path.dirname(build_ext.get_ext_fullpath('x'))
            try:
                os.makedirs(target)
            except OSError:
                pass

            target = os.path.join(target, dest)
            for filename in os.listdir(dylib_path):
                if filename.endswith(DYNAMIC_LIB_SUFFIX):
                    shutil.copy(os.path.join(dylib_path, filename),
                                os.path.join(target, filename))


def build_rust_cmdclass(crates, debug=False,
                        extra_cargo_args=None, quiet=False):
    class _RustBuildCommand(RustBuildCommand):
        rust_build_args = {
            'cargo_crates': crates,
            'debug': debug,
            'extra_cargo_args': extra_cargo_args,
            'quiet': quiet,
        }
    return _RustBuildCommand


def build_install_lib_cmdclass(base=None):
    if base is None:
        base = install_lib
    class _RustInstallLibCommand(base):
        def build(self):
            base.build(self)
            if not self.skip_build:
                self.run_command('build_rust')
    return _RustInstallLibCommand


def install_lib_cmdclass(base=None):
    if base is None:
        base = install_lib
    class _RustInstallLibCommand(base):
        def build(self):
            base.build(self)
    return _RustInstallLibCommand
