# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['lapi']
install_requires = \
['pynacl>=1.5.0,<2.0.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'lapi',
    'version': '0.1.1',
    'description': 'Lamden API',
    'long_description': '````python\nfrom lapi import LAPI, Wallet\n\nprivate_key = \'27ae87946a3dcf563692a9ed7957401acd3ff55349d8eabd9b9b6c635ae6d29f\'\nwallet = Wallet(private_key)\nlapi = LAPI(wallet=wallet)\n\ntx = lapi.send(amount=1, to_address=\'4489524c8d7a36a488d1be063af1d89ccc57d6aabb58e75badf0f020621dd0cc\')\n\nprint(tx)\n\nkwargs = {\n    "amount": 1,\n    "to": \'4489524c8d7a36a488d1be063af1d89ccc57d6aabb58e75badf0f020621dd0cc\'\n}\n\ntx = lapi.post_tx(200, contract=\'currency\', function=\'transfer\', kwargs=kwargs)\n\nprint(tx)\n````\n',
    'author': 'Endogen',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
