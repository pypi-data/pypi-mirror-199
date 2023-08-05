# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['virttop']

package_data = \
{'': ['*']}

install_requires = \
['defusedxml>=0.7.1,<0.8.0', 'libvirt-python>=9.0.0,<10.0.0']

entry_points = \
{'console_scripts': ['virttop = virttop.virttop:main']}

setup_kwargs = {
    'name': 'virttop',
    'version': '0.2.2',
    'description': 'A top like utility for libvirt',
    'long_description': "# virttop\na top like utility for libvirt\n\n![Image](virttop.png)\n\n## How to get\n```sh\npip install virttop\n```\n\n## Options\n```sh\nusage: virttop.py [-h] [--uri URI [URI ...]] [--config CONFIG]\n                  [--active ACTIVE] [--logfile LOGFILE]\n\noptions:\n  -h, --help            show this help message and exit\n  --uri URI [URI ...], -u URI [URI ...]\n                        A list of URIs to connect to seperated by commas\n  --config CONFIG, -c CONFIG\n                        Path to the config file\n  --active ACTIVE, -a ACTIVE\n                        Show active VMs only\n  --logfile LOGFILE, -l LOGFILE\n                        Location of the log file\n```\n\n## Configfile\nThe default location for the config file is '~/.virttop.toml'.\n\n```toml\n[color]\nname_column_fg=23\nname_column_bg=0\nactive_row_fg=24\nactive_row_bg=0\ninactive_row_fg=244\ninactive_row_bg=0\nbox_fg=29\nbox_bg=0\nselected_fg=0\nselected_bg=36\n```\n\n## Keybindings\n\n`j`,`k` and arrow keys move up and down.\n\n`g` moves to the top of the list.\n\n`G` moves to the bottom of the list.\n\n`r` runs an inactive domain.\n\n`s` shuts down a running domain.\n\n`d` destroys a running domain.\n",
    'author': 'terminaldweller',
    'author_email': 'devi@terminaldweller.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/terminaldweller/virttop',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
