# This file is placed in the Public Domain.


import os


from setuptools import setup


def read():
    return open("README.rst", "r").read()


setup(
    name='libobj',
    version='410',
    url='https://github.com/bthate/libobj',
    author='Bart Thate',
    author_email='bthate@dds.nl', 
    description="python3 object library",
    long_description=read(),
    long_description_content_type='text/x-rst',
    license='Public Domain',
    package_dir={
                  "": "lib",
                 },
    py_modules=['obj'],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
