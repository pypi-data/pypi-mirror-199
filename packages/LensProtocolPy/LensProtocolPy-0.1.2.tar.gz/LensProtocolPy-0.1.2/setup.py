from setuptools import find_packages, setup
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='LensProtocolPy',
    packages=["lenspy"],
    version='0.1.2',
    description='A python library for working with Lens Protocol',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Rishin Madan and Tobias Loader',
    license='MIT',
    install_requires = ["gql", "requests-toolbelt"],
    package_data={'lenspy': ['*']}
)
