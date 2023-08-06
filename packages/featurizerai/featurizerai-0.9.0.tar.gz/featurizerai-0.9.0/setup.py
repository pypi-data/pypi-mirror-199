import setuptools
from setuptools import *

setup(
    name='featurizerai',
    version='0.9.0',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    install_requires=[
        'requests',
    ],
    author='Featurizer AI',
    license='MIT',
    python_requires='>=3.6',
    test_suite='tests',
)
