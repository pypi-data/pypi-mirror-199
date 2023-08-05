# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['katia',
 'katia.interpreter',
 'katia.logger_manager',
 'katia.message_manager',
 'katia.recognizer',
 'katia.speaker']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==6.0',
 'boto3==1.26.90',
 'confluent-kafka==2.0.2',
 'googletrans==3.1.0a0',
 'openai==0.27.2',
 'pyaudio==0.2.13',
 'pygame==2.2.0',
 'python-dotenv==1.0.0',
 'speechrecognition==3.9.0']

setup_kwargs = {
    'name': 'katia',
    'version': '0.1.1',
    'description': 'Katia is a wonderfull assistant created for help people to iteract with the digital world',
    'long_description': '.. _topics-index:\n\n============\nKatia Readme\n============\n\n.. image:: https://katia.readthedocs.io/en/latest/_images/logo.png\n    :align: center\n    :alt: logo\n    :height: 300px\n\n|\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n\n.. image:: https://github.com/martingaldeca/Katia/actions/workflows/linters.yml/badge.svg?event=push\n    :target: https://github.com/martingaldeca/Katia/actions\n    :alt: Linters\n\n.. image:: https://github.com/martingaldeca/Katia/actions/workflows/tests.yml/badge.svg?event=push\n    :target: https://github.com/martingaldeca/Katia/actions\n    :alt: Tests\n\n.. image:: https://coveralls.io/repos/github/martingaldeca/Katia/badge.svg?branch=master\n    :target: https://coveralls.io/github/martingaldeca/Katia?branch=master\n    :alt: Coverage\n\n.. image:: https://img.shields.io/pypi/v/katia.svg\n    :target: https://pypi.org/project/katia/\n    :alt: PyPI\n\n.. image:: https://readthedocs.org/projects/katia/badge/\n    :target: https://katia.readthedocs.io/en/latest/\n    :alt: docs\n\nKatia is a python project ment to be used as a package to create assistants where they are\nneeded.\n\nIt is based on the top techs in the market. It uses ``OPENAI API`` to understand what are\nyou telling to her/him. To speak with you he/she uses ``AWS Polly``. And, to heard what are\nyou telling to him/her he/she uses ``Google recognizer``.\n\nYo can check the code in `GitHub <https://github.com/martingaldeca/Katia>`_ or follow the\n`official documentation <https://katia.readthedocs.io/en/latest/>`_.',
    'author': 'martingaldeca',
    'author_email': 'martingaldeca@gmail.com',
    'maintainer': 'martingaldeca',
    'maintainer_email': 'martingaldeca@gmail.com',
    'url': 'https://katia.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
