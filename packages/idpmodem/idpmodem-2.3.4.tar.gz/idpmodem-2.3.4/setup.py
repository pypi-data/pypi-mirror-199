# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idpmodem',
 'idpmodem.asyncio',
 'idpmodem.codecs',
 'idpmodem.codecs.common_message_format',
 'idpmodem.codecs.common_message_format.fields',
 'idpmodem.threaded']

package_data = \
{'': ['*']}

install_requires = \
['aioserial==1.3.0', 'pyserial-asyncio>=0.6,<0.7', 'pyserial>=3.5,<4.0']

setup_kwargs = {
    'name': 'idpmodem',
    'version': '2.3.4',
    'description': 'A library for interfacing with an Inmarsat IsatData Pro satellite IoT modem using serial AT commands.',
    'long_description': None,
    'author': 'geoffbrucepayne',
    'author_email': 'geoff.bruce-payne@inmarsat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
