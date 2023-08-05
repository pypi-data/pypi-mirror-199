# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['magnify']

package_data = \
{'': ['*']}

install_requires = \
['basicpy>=1.0.1,<2.0.0',
 'catalogue>=2.0.8,<3.0.0',
 'dask[complete]>=2022.02.0',
 'numpy>=1.21.0,<2.0.0',
 'pandas>=1.3.0,<2.0.0',
 'scipy>=1.9.0,<2.0.0',
 'tifffile>=2021.11.2',
 'tqdm>=4.64,<5.0',
 'types-tqdm>=4.64,<5.0',
 'xarray[complete]>=2023.01.0']

extras_require = \
{':sys_platform != "darwin"': ['opencv-python>=4.0'],
 ':sys_platform == "darwin"': ['opencv-python>=4.0,!=4.7.0.68']}

setup_kwargs = {
    'name': 'magnify',
    'version': '0.1.8',
    'description': 'A microscopy image processing toolkit.',
    'long_description': '# magnify\nA microscopy image processing toolkit.\n',
    'author': 'Karl Krauth',
    'author_email': 'karl.krauth@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
