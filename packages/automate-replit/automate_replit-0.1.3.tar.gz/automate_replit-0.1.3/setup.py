# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autoreplit', 'autoreplit.classes']

package_data = \
{'': ['*'], 'autoreplit': ['gql/*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0', 'aiolimiter==1.0.0']

setup_kwargs = {
    'name': 'automate-replit',
    'version': '0.1.3',
    'description': 'Automate your replit account using this replit api wrapper!',
    'long_description': '# Automate Replit\n[![Documentation Status](https://readthedocs.org/projects/automate-replit/badge/?version=latest)](https://automate-replit.readthedocs.io/en/latest/?badge=latest)\n\n\nAutomate replit actions with this replit api wrapper!\n\n## Docs\nDocumentation for this library can be found [here](https://automate-replit.readthedocs.io/en/docs/)\n\n## Source\nSource can be found [here](https://github.com/thatrandomperson5/automate-replit)\n\n## Example\n```py\nfrom autoreplit import ReplitClient\n\nclient = ReplitClient()\n\nasync def getEthan():\n    ethan = await client.getUserByName("not-ethan")\n    print(f"Ethan\'s id: {ethan.id}")\n    print(f"Ethan\'s follower count: {ethan.followerCount}")\n    if ethan.isOnline:\n        print("Ethan is online!")\n    else:\n        print(f"Ethan was last seen {ethan.lastSeen}")\n    print(f"Ethan\'s roles: {ethan.roles}")\n    print(f"All of ethan: {ethan}")\n\nclient.run(getEthan())\n```\n**Note**: pass a sid to get better info',
    'author': 'thatrandomperson5',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/thatrandomperson5/automate-replit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.0,<4.0.0',
}


setup(**setup_kwargs)
