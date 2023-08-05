#===============================================================================#
# Script Name: setup.py                                                         #
#                                                                               #
# Description: ensures all toolboxes necessary are downloaded                   #
#                                                                               #
# Author:      Jen Burrell (March 8th, 2023)                                    #
#===============================================================================#
import os.path as op
from setuptools import setup
from setuptools import find_namespace_packages
from setuptools import Command

# - setup.py file's home directory - #
basedir = op.dirname(__file__)

# - Get Version - #
version = {}
with open(op.join(basedir, "src/ConCorr/version.py")) as f:
    for line in f:
        if line.startswith('__version__'):
            exec(line, version)
            break
version = version['__version__']

# - Readme - #
with open(op.join(basedir, 'README.rst'), 'rt') as f:
    readme = f.read()

# - Dependencies are listed in requirements.txt - #
#with open(op.join(basedir, 'requirements.txt'), 'rt') as f:
#    install_requires = [l.strip() for l in f.readlines()]

# - set it up! - #
setup(
    name='ConCorr',
    version=version,
    description='A small fMRI functional connectivity toolbox',
    long_description=readme,
    long_description_content_type='text/x-rst',
    url='https://github.com/jenburrell/ConCorr',
    author='Jen Burrell',
    author_email='jenbur@psych.ubc.ca',
    python_requires='>=3.10',
    
    package_dir={"":"src"},
    packages=find_namespace_packages(where='src'),
    
    classifiers=[
    'Programming Language :: Python :: 3.10',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    
    install_requires=[
        'numpy>=1',
        'scipy>=1.9.3',
        'pandas>=1.5.0',
        'seaborn>=0.12.1',
        'matplotlib>=3.6.0',
        'pingouin>=0.5.3',
        'scikit-learn>=1.0.2',
        'fastcluster>=1.2.6',
    ],
    extras_require={
        "dev": [
            "pytest>=3.7",
        ],
    },
)



### --- BEFORE PUBLISHING --- ###
# check-manifest --create
# git add MANIFEST.in

# python setup.py sdist # to do source distribution
# tar tzf dist/ConCorr-0.0.1.tar.gz # should show lots of files see pic

### --- TO PUBLISH --- ###
# python setup.py bdist_wheel sdist
# python install twine
# python upload dist/*
