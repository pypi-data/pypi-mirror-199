# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyqt_feedback_flow']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.6,<6.0.0', 'emoji>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'pyqt-feedback-flow',
    'version': '0.2.0',
    'description': 'Show feedback in toast-like notifications',
    'long_description': '# pyqt-feedback-flow --- Show feedback in toast-like notifications\n\n---\n\n[![PyPI Version](https://img.shields.io/pypi/v/pyqt-feedback-flow.svg)](https://pypi.python.org/pypi/pyqt-feedback-flow)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyqt-feedback-flow.svg)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/pyqt-feedback-flow.svg)\n[![Downloads](https://pepy.tech/badge/pyqt-feedback-flow)](https://pepy.tech/project/pyqt-feedback-flow)\n[![GitHub license](https://img.shields.io/github/license/firefly-cpp/pyqt-feedback-flow.svg)](https://github.com/firefly-cpp/pyqt-feedback-flow/blob/master/LICENSE)\n![GitHub commit activity](https://img.shields.io/github/commit-activity/w/firefly-cpp/pyqt-feedback-flow.svg)\n[![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/firefly-cpp/pyqt-feedback-flow.svg)](http://isitmaintained.com/project/firefly-cpp/pyqt-feedback-flow "Average time to resolve an issue")\n[![Percentage of issues still open](http://isitmaintained.com/badge/open/firefly-cpp/pyqt-feedback-flow.svg)](http://isitmaintained.com/project/firefly-cpp/pyqt-feedback-flow "Percentage of issues still open")\n[![Fedora package](https://img.shields.io/fedora/v/python3-pyqt-feedback-flow?color=blue&label=Fedora%20Linux&logo=fedora)](https://src.fedoraproject.org/rpms/python-pyqt-feedback-flow)\n\n![Pyqt](https://user-images.githubusercontent.com/73126820/167383927-6fe17311-4e80-42fc-a0ef-1494b4c58762.png)\n\n## Description\nOn many occasions, notifications can be a valuable tool to inform a user about specific events. Sometimes, static notifications or pop-up windows may provide adequate feedback; however, there are some cases where flowing notifications can be more appropriate.\n\nThis software allows us to show flowing notifications in the realm of a text or a picture. Both text and pictures (raster and vector) can be customized according to users\' wishes, which offers a wide variety of possibilities for providing flowing feedback.\n\n## Text notification example\nhttps://user-images.githubusercontent.com/73126820/167379237-7c85467d-133e-42c9-91fd-7e85f2481267.mp4\n\n## Image notification example\nhttps://user-images.githubusercontent.com/73126820/167380818-814cc1ce-d137-4906-b5a4-84af94c46d4a.mp4\n\n## Installation\n\n### pip\n\nInstall this software with pip:\n\n```sh\npip install pyqt-feedback-flow\n```\n\n### Alpine Linux\n\nTo install pyqt-feedback-flow on Alpine Linux, use:\n\n```sh\n$ apk add py3-pyqt-feedback-flow\n```\n\n### Arch Linux\n\nTo install pyqt-feedback-flow on Arch Linux, please use an [AUR helper](https://wiki.archlinux.org/title/AUR_helpers):\n\n```sh\n$ yay -Syyu python-pyqt-feedback-flow\n```\n\n### Fedora Linux\n\nTo install pyqt-feedback-flow on Fedora Linux, use:\n\n```sh\n$ dnf install python3-pyqt-feedback-flow\n```\n\n## License\n\nThis package is distributed under the MIT License. This license can be found online at <http://www.opensource.org/licenses/MIT>.\n\n## Disclaimer\n\nThis framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!\n',
    'author': 'Iztok Fister Jr.',
    'author_email': 'iztok@iztok-jr-fister.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/firefly-cpp/pyqt-feedback-flow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
