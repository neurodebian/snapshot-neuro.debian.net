#!/usr/bin/python

from distutils.core import setup, Extension

module1 = Extension('hasher',
                    define_macros = [('_LARGEFILE64_SOURCE', 1)],
                    sources = ['hasher.c'],
                    libraries = ['crypto'])

setup (name = 'Hasher',
       version = '1.0',
       description = 'module to hash a file',
       ext_modules = [module1])

# vim:set ts=4:
# vim:set et:
# vim:set shiftwidth=4:
