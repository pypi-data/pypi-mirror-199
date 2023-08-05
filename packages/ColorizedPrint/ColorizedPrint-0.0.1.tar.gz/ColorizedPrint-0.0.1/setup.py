from setuptools import setup
import setuptools

longDescription = 'This is a modified version of a print function of a python'

setup(
    name='ColorizedPrint',
    version='0.0.1',
    description=longDescription,
    author='Abhay Vachhani',
    packages=setuptools.find_packages(),
    py_modules=['ColorizedPrint'],
    package_dir={'': 'src'},
    install_requires=[
        'colorama'
    ]
)