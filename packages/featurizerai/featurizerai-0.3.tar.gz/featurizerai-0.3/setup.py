from setuptools import setup, find_packages

setup(
    name='featurizerai',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Featurizer AI',
    license='MIT',
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
