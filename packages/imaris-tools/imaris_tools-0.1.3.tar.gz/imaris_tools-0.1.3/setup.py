import os
import sys
import shutil
from setuptools import setup
from warnings import warn

if sys.version_info.major != 3:
    raise RuntimeError('imaris_tools requires Python 3')


setup(name='imaris_tools',
      version='0.1.3',
      description='manipulation of ims files',
      author='',
      author_email='',
      package_dir={'': 'src'},
      packages=['imaris_tools'],
      install_requires=[
          'numpy',
          'datatable',
          'h5py',
          ],
      scripts=['src/imaris_tools/ims2csv.py'],
      )


# get location of setup.py
setup_dir = os.path.dirname(os.path.realpath(__file__))
