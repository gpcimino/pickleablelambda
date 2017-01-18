#!/usr/bin/env python

import setuptools


setuptools.setup(
    name='pickleablelambda',
    version='0.1',

    # This automatically detects the packages in the specified
    # (or current directory if no directory is given).
    packages=setuptools.find_packages(),

    zip_safe=False,

    author='Giampaolo Cimino',
    author_email='gcimino@gmail.com',

    description='Make lambda functions pickleable',

    # For this parameter I would recommend including the
    # README.rst
    long_description='''Using a proxy class lambda functions can be pickled and unpickled.''',

    # The license should be one of the standard open source
    # licenses: https://opensource.org/licenses/alphabetical
    license='MIT',

    test_suite = 'tests',

    install_requires=[
        'dill'
    ]
    
    )
