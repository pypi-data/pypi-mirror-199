from setuptools import find_packages, setup

setup(
    name='ppdb_auth_lib',
    packages=find_packages(include=['ppdb_auth_lib']),
    version='0.1.9',
    description='Auth Library PPDBV2',
    author='mrizkyff',
    license='MIT',
    install_requires=[
        'pyjwt',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='test'
)