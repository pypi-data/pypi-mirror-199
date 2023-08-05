from setuptools import setup
import setuptools

longDescription = 'This is a modified version of a print function of a python'

setup(
    name='ColorizedPrint',
    version='0.0.2',
    keywords=['Abhay', 'Abhay Vachhani', 'Abhay28', 'Colorized Print', 'ColorizedPrint', 'print'],
    description=longDescription,
    author='Abhay Vachhani',
    packages=setuptools.find_packages(),
    py_modules=['ColorizedPrint'],
    package_dir={'': 'src'},
    install_requires=[
        'colorama'
    ]
)