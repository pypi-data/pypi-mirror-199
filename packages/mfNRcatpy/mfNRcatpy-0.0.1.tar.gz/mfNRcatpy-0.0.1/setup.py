from setuptools import setup, find_packages
find_packages(where='mfNRcatpy')

setup(
    name='mfNRcatpy',
    version='0.0.1',
    packages=find_packages() + find_packages(where='mfNRcatpy'),
    install_requires=['numpy',
                      'scipy',
                      'core-watpy',
                      'h5py',
                      'matplotlib',
                      'lalsuite',
                      'numba'],
    author = 'Sebastian Gomez Lopez',
    author_email= 'segomezlo@unal.edu.co',
    url = 'https://github.com/sebastiangomezlopez/mfNRcatpy'

    )
