from setuptools import setup, find_packages
import os

setup(
    name='pyqt-units',
    packages=find_packages(exclude=[]),
    version='3.1',
    description='System of units for PyQt',
    author='Neil Butcher',
    url='https://github.com/ergoregion/pyqt-units.git',
    license='MIT',
    keywords=['units pyqt measurements'],
    install_requires=[],
    python_requires='>=3',
    package_data={
        'pyqt_units': [os.path.join('measurements','measurements_root.db')],
    },
    classifiers=[],
)
