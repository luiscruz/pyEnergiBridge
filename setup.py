from setuptools import setup, find_packages
import os

# Determine the platform-specific binary directory
bin_dir = os.path.join('bin', 'energibridge')

setup(
    name='pyEnergiBridge',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': [bin_dir],
    },
    install_requires=[
    ],
)