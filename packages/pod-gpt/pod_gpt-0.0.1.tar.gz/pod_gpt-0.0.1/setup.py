# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pod_gpt']

package_data = \
{'': ['*']}

install_requires = \
['langchain>=0.0.125,<0.0.126']

setup_kwargs = {
    'name': 'pod-gpt',
    'version': '0.0.1',
    'description': 'Package for building podcast search indexes.',
    'long_description': '# PodGPT',
    'author': 'James Briggs',
    'author_email': 'james@aurelio.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
