# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crop_clip']

package_data = \
{'': ['*']}

install_requires = \
['h5py>=3.7.0,<4.0.0',
 'numpy>=1.24.2,<2.0.0',
 'pillow>=9.4.0,<10.0.0',
 'pydantic>=1.10.7,<2.0.0',
 'tqdm>=4.65.0,<5.0.0']

entry_points = \
{'console_scripts': ['crop_clip = crop_clip:crop_clip.main']}

setup_kwargs = {
    'name': 'crop-clippier',
    'version': '0.0.1',
    'description': 'A tool for cropping regions out of volumetric data',
    'long_description': '',
    'author': 'Matthew Pimblott',
    'author_email': 'Matthew.Pimblott@diamond.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
