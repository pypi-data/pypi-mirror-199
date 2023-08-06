import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='popupsort',
    version='1.2',
    description='A Python package for visualizing sorting algorithms',
    long_description = README,
    long_description_content_type="text/markdown",
    author='Zouheir Nakouzi',
    author_email='zouheir2002@gmail.com',
    url='https://github.com/ZouheirN/PopUpSort',
    packages=['popupsort'],
    license='MIT',
    license_files = ('LICENSE.md',),
    zip_safe=False
)
