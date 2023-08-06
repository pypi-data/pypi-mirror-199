from setuptools import setup, find_packages

python_version = '>=3.7'

install_requires = [
    'numpy',
    'scipy',
    'sympy',
    'tabulate',
    'irrep',
    'qsymm',
    'matplotlib'
]

# uses README.md as the package long description
with open("README.md") as f:
    long_description = f.read()

setup(
    name="TESTEKP",
    description="...",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=0.32,
    packages=find_packages('.'),
    install_requires=install_requires,
    python_requires=python_version
    #licence=
    #classifiers=
)
