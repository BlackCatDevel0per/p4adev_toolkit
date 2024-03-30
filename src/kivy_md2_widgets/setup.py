# -*- coding: utf-8 -*-
# TODO: Publish to PyPi..
# auto-generated (setup.py need for p4a recipe to build by buildozer)
# you can also use p4a-recipes package from PyPi
from setuptools import setup

packages = [
    'kivy_md2_widgets',
    'kivy_md2_widgets.pickers',
    'kivy_md2_widgets.pickers.themepicker',
]

package_data = {
    '':
        [
            '*'
        ]
}

setup_kwargs = {
    'name': 'kivy_md2_widgets',
    'version': '0.0.0',
    'description': '...',
    'long_description': 'None',
    'author': 'BlackCatDevel0per',
    'author_email': 'bcdev@mail.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
