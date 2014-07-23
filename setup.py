try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='RNA_TwiZe',
    version='0.1.9',
    author='Will Blevins and Andres Lanzos Camionai',
    author_email='willblev@gmail.com',
    packages=['rna_twize','rna_twize_test'],
    license='LICENSE.txt',
    description='RNA Twilight-Zone Curve Maker.',
    long_description=open('README.txt').read(),
    requires=[
    "Bio",
    "Tkinter",
    "tkFileDialog",
    "tkMessageBox",
    "re",
    "urllib",
    "numpy",
    "pylab",
    "sys",
    "os",
],
)
