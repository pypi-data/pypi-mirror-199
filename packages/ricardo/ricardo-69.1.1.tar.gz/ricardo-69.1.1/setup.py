# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ricardo']

package_data = \
{'': ['*'], 'ricardo': ['assets/*']}

setup_kwargs = {
    'name': 'ricardo',
    'version': '69.1.1',
    'description': "Ricardo. But it's Python.",
    'long_description': "# Ricardo\n\n'cause that's a good meme.\n",
    'author': 'Predeactor',
    'author_email': 'pro.julien.mauroy@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
