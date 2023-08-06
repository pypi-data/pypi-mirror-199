# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['led_cube_view', 'led_cube_view.tools']

package_data = \
{'': ['*'], 'led_cube_view': ['config/*']}

install_requires = \
['PyOpenGL>=3.1.6,<4.0.0',
 'QtPy>=2.3.0,<3.0.0',
 'numpy-stl>=3.0.0,<4.0.0',
 'pyqtgraph>=0.13.1,<0.14.0']

setup_kwargs = {
    'name': 'led-cube-view',
    'version': '1.1.2',
    'description': 'A QtPy widget to display a LED cube on a 3D graph and manipulate its LEDs.',
    'long_description': '# led-cube-view\nA QtPy widget to display a LED cube on a 3D graph and manipulate its LEDs.\nThis is being developed for use with my [LED cube editor](https://github.com/crash8229/led-cube-editor).\n',
    'author': 'crash8229',
    'author_email': 'mu304007@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/crash8229/led-cube-view',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
