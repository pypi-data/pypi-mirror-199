# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_saa', 'nonebot_plugin_saa.nonebug']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-plugin-send-anything-anywhere>=0.2.2,<0.3.0',
 'nonebug>=0.3.1,<0.4.0',
 'pytest-mock>=3.10.0,<4.0.0']

entry_points = \
{'pytest11': ['saa_nonebug = nonebot_plugin_saa.nonebug.fixtures']}

setup_kwargs = {
    'name': 'nonebot-plugin-send-anything-anywhere-nonebug',
    'version': '0.1.0a0',
    'description': 'A nonebug helper for nonebot-plugin-send-anything-anything',
    'long_description': '<div align="center">\n\n~logo征集中，假装有图片~\n\n# Nonebot Plugin<br>Send Anything Anywhere\n### nonebug helper\n\n你只管业务实现，把发送交给我们\n\n</div>\n',
    'author': 'felinae98',
    'author_email': 'me@felinae98.cn',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/felinae98/nonebot-plugin-send-anything-anywhere-nonebug',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
