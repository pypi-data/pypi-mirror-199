# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['omf', 'omf.fileio', 'omf.scripts']

package_data = \
{'': ['*']}

install_requires = \
['geoh5py==0.5.0',
 'numpy>=1.7,<2.0',
 'properties>=0.6.0,<0.7.0',
 'pypng>=0.20220715,<0.20220716',
 'six>=1.16,<2.0',
 'vectormath>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['geoh5_to_omf = omf.scripts.geoh5_to_omf:run',
                     'omf_to_geoh5 = omf.scripts.omf_to_geoh5:run']}

setup_kwargs = {
    'name': 'mira-omf',
    'version': '3.0.0a4',
    'description': 'API Library for Open Mining Format',
    'long_description': 'omf\n***\n\n.. image:: https://img.shields.io/pypi/v/mira-omf.svg\n    :target: https://pypi.python.org/pypi/mira-omf\n    :alt: Latest PyPI version\n\n.. image:: https://readthedocs.org/projects/omf/badge/?version=stable\n    :target: http://omf.readthedocs.io/en/stable/\n    :alt: Documentation\n\n.. image:: https://img.shields.io/badge/license-MIT-blue.svg\n    :target: https://github.com/MiraGeoscience/omf/blob/main/LICENSE\n    :alt: MIT license\n\n.. image:: https://github.com/MiraGeoscience/omf/actions/workflows/pytest-windows.yml/badge.svg\n    :target: https://github.com/MiraGeoscience/omf/actions/workflows/pytest-windows.yml\n    :alt: pytest\n\n\nVersion: 3.0.0-alpha.4\n\nAPI library for Open Mining Format, a new standard for mining data backed by\nthe `Global Mining Standards & Guidelines Group <http://www.globalminingstandards.org/>`_.\n\n.. warning::\n    **Pre-Release Notice**\n\n    This is a Beta release of the Open Mining Format (OMF) and the associated\n    Python API. The storage format and libraries might be changed in\n    backward-incompatible ways and are not subject to any SLA or deprecation\n    policy.\n\n.. warning::\n    **Alpha-Release Notice**\n\n    This is a fork created by Mira Geoscience for interoperability with the\n    geoh5 file format.\n\nWhy?\n----\n\nAn open-source serialization format and API library to support data interchange\nacross the entire mining community.\n\nScope\n-----\n\nThis library provides an abstracted object-based interface to the underlying\nOMF serialization format, which enables rapid development of the interface while\nallowing for future changes under the hood.\n\nGoals\n-----\n\n- The goal of Open Mining Format is to standardize data formats across the\n  mining community and promote collaboration\n- The goal of the API library is to provide a well-documented, object-based\n  interface for serializing OMF files\n\nAlternatives\n------------\n\nOMF is intended to supplement the many alternative closed-source file formats\nused in the mining community.\n\nConnections\n-----------\n\nThis library makes use of the `properties <https://github.com/seequent/properties>`_\nopen-source project, which is designed and publicly supported by\n`Seequent <https://seequent.com>`_.\n\nConnection to the geoh5 format makes use of `geoh5py <https://geoh5py.readthedocs.io/>`_\npublicly supported by `Mira Geoscience <https://mirageoscience.com/>`_\n\nInstallation\n------------\n\nTo install the repository, ensure that you have\n`pip installed <https://pip.pypa.io/en/stable/installing/>`_ and run:\n\n.. code:: bash\n\n    pip install omf\n\nOr from `github <https://github.com/GMSGDataExchange/omf>`_:\n\n.. code:: bash\n\n    git clone https://github.com/GMSGDataExchange/omf.git\n    cd omf\n    pip install -e .\n',
    'author': 'Mira Geoscience',
    'author_email': 'dominiquef@mirageoscience.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://www.globalminingstandards.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<3.11',
}


setup(**setup_kwargs)
