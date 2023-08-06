from pathlib import Path
from typing import Final
from setuptools import setup, find_packages

SOURCE_DIRECTORY: Final = 'src'
PACKAGE_NAME: Final = 'vrplib_reader'
VERSION: Final = '0.0.3'
THIS_DIRECTORY: Final = Path(__file__).parent
LONG_DESCRIPTION: Final = (THIS_DIRECTORY / "README.md").read_text()
PACKAGES: Final = find_packages(where=SOURCE_DIRECTORY,
                                exclude=[
                                    'interfaces',
                                    'readers'
                                    f'{PACKAGE_NAME}.interfaces',
                                    f'{PACKAGE_NAME}.readers']
                                )

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    url='https://github.com/nicosnow-cl/vrplib-reader',
    author='Nicolás Frías',
    author_email='nicolas.friasrojas@gmail.com',
    package_dir={'': SOURCE_DIRECTORY},
    packages=PACKAGES,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown'
)
