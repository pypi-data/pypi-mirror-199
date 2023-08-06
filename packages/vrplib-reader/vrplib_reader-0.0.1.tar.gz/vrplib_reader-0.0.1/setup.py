from pathlib import Path
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='vrplib_reader',
    version="0.0.1",
    url='https://github.com/nicosnow-cl/vrplib-reader',
    author='Nicolás Frías',
    author_email='nicolas.friasrojas@gmail.com',
    packages=['src'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
