#!/usr/bin/env python

import setuptools
import os

__version__ = '0.1.0'

# Find the absolute path
here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.md')) as f:
    long_description = f.read()

short_description = 'QC_run: An API for submitting popular  quantum chemistry programs to a slurm queue system'

setuptools.setup(name='QC_run',
      version=__version__,
      maintainer='Stefan Vogt',
      maintainer_email='stvogtgeisse@gmail.com',
      description=short_description,
      long_description=long_description,
      url='', # Git in feynman
      license='MIT',
      install_requires=[
      ],
      packages=['qc_run'],
      #entry_points={
      #    'console_scripts': ['calculate_rmsd=rmsd.calculate_rmsd:main']
      #},
)
