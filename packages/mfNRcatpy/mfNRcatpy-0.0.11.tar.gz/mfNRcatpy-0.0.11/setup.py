from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
ld = (this_directory / "README.md").read_text()
print(ld)

find_packages(where='mfNRcatpy')

setup(
    name='mfNRcatpy',
    version='0.0.11',
    long_description=ld,
    long_description_content_type='text/markdown',
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
