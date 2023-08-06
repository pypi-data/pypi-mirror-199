import os
from setuptools import setup, find_packages

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
readme_path = os.path.join(parent_dir, "README.md")

with open(readme_path, "rt") as f:
    readme = f.read()

VERSION = '0.0.17' 
DESCRIPTION = "Find what you're looking for in a flash with Huntela."
LONG_DESCRIPTION = readme

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="huntela", 
    version=VERSION,
    author="Tomisin Abiodun",
    author_email="decave.12357@gmail.com",
    description=DESCRIPTION,
    url='https://github.com/CodeLexis/huntela',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['psutil'], # add any additional packages that 
    # needs to be installed along with your package. Eg: 'caer'
    python_requires=">=3.9, <4",
    keywords=['python', 'search', 'query'],
    classifiers= [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development :: Libraries"
    ]
)
