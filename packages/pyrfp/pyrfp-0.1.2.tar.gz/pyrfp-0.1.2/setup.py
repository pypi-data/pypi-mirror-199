# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrfp']

package_data = \
{'': ['*']}

install_requires = \
['pyapes>=0.2.1,<0.3.0', 'pymaxed>=0.1.7,<0.2.0', 'pymytools>=0.1.12,<0.2.0']

setup_kwargs = {
    'name': 'pyrfp',
    'version': '0.1.2',
    'description': 'Python package for the data-driven Rosenbluth-Fokker-Planck equation.',
    'long_description': "# Python Package for the Rosenbluth Fokker Planck (RFP) Equation\n\n> Currently, heavily under renovation (refactoring) from my old code (in my other private repository)\n\n## Description\n\nThis package is refactored version of a part of the `pystops_ml` code.\nI've separated only data generation and training part from `pystops_ml`.\n\nUnlike `pystops_ml`, this module doesn't utilize distributed training. (`DDP` feature not needed)\n\nThis code is part of my paper, Data-Driven Stochastic Particle Scheme for Collisional Plasma Simulations.\n\n- Preprint is available at [SSRN](https://ssrn.com/abstract=4108990)\n\n## Features\n\n- Data generation\n  - Uncertainty quantification using the maximum entropy distribution (using `pymaxed`)\n  - Axisymmetric evaluation of the Rosenbluth potentials and their derivatives\n- Data training: supports `cpu`, `cuda`, and `mps` training\n- Data-driven simulation: `rfp-ann`\n\n## Installation\n\nYou can install via `pip`\n\n```bash\n$python3 -m pip install pyrfp\n```\n\n## Dependencies\n\n- Global\n- `python >=3.10`\n- `torch >= 1.13.1`\n\n- Personal project\n  - `pymaxed` (for the Maximum Entropy Distribution)\n  - `pyapes` (for the field solver)\n  - `pymytools` (miscellaneous tools including data IO, logging, and progress bar)\n",
    'author': 'Kyoungseoun Chung',
    'author_email': 'kyoungseoun.chung@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
