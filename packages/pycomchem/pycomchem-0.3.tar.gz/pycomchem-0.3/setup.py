# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['comchem']

package_data = \
{'': ['*']}

install_requires = \
['cairosvg>=2.5.2,<3.0.0']

setup_kwargs = {
    'name': 'pycomchem',
    'version': '0.3',
    'description': 'Python library for accessing the CommonChemistry.org API',
    'long_description': '## pyComChem\nA Python package to access data via the CommonChemistry.org API.\n\nA revised version of the CommonChemistry website, originally at commonchemistry.org, has been redeveloped\ninto a much larger (~500K) database of CAS Registry Numbers and now includes an API for programmatic access.\n\nThis package provides access to the API to search the database and extract chemical metadata, images, and mol files.\n\nCurrently available commands are:\n\n- query - search either and exact string or substring\n- detail - full metadata retrieval\n- key2cas - specialized function to return the CAS Registry Number of a compound from its InChIKey\n- chemimg - download structural images an `.svg`, `.png`, or `.ps` files\n\nFuture improvements will include\n\n- molfile - download the mol file of a compound\n- additional specialized functions\n',
    'author': 'Stuart Chalk',
    'author_email': 'schalk@unf.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/stuchalk/pyComChem',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
