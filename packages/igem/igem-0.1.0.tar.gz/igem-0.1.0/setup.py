# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['igem',
 'igem.epc',
 'igem.epc.clarite',
 'igem.epc.clarite.analyze',
 'igem.epc.clarite.describe',
 'igem.epc.clarite.load',
 'igem.epc.clarite.modify',
 'igem.epc.clarite.plot',
 'igem.epc.clarite.survey',
 'igem.ge',
 'igem.ge.db',
 'igem.ge.etl',
 'igem.ge.filter',
 'igem.ge.forms',
 'igem.ge.management',
 'igem.ge.management.commands',
 'igem.ge.management.commands.olds',
 'igem.ge.migrations',
 'igem.ge.views',
 'igem.omics',
 'igem.omics.db',
 'igem.omics.management',
 'igem.omics.management.commands',
 'igem.omics.migrations',
 'igem.src']

package_data = \
{'': ['*'],
 'igem': ['base_static/global/css/*',
          'base_static/global/js/*',
          'base_templates/global/*',
          'base_templates/global/partials/*',
          'psa/*',
          'psa/ctd/ctdcgint/*'],
 'igem.ge': ['templates/ge/pages/*', 'templates/ge/partials/*']}

install_requires = \
['black>=23.1.0,<24.0.0',
 'clarite>=2.3,<3.0',
 'django-debug-toolbar>=3.8.1,<4.0.0',
 'django-thread>=0.0.1,<0.0.2',
 'django>=4.1.5,<5.0.0',
 'mypy>=0.991,<0.992',
 'patool>=1.12,<2.0',
 'psycopg2>=2.9.5,<3.0.0',
 'pytest>=7.2.1,<8.0.0',
 'requests>=2.28.2,<3.0.0',
 'types-requests>=2.28.11.8,<3.0.0.0']

setup_kwargs = {
    'name': 'igem',
    'version': '0.1.0',
    'description': '',
    'long_description': '\n\n------------\n\n\n------------\n\nIGEM: \n==============================================================================\n\n* Free software: 3-clause BSD license\n\nExamples\n--------\n**Main screen for master data registration:**\n\n.. image:: docs/source/_static/example/web_add.png\n\n|\n\n**The query for links between terms found while ingesting an external dataset:**\n\n.. image:: docs/source/_static/example/web_key.png\n\n\nInstallation\n------------\nThe IGEM system ran on Python and was built on DJANGO for database management and web interface.\n\nTo run the system, copy the /src folder to the desired location with access to Python > 3.7 and the packages described in the requirements.\n\nThe IGEM system can use any database supported by Django. You will need to set the database in the /src/src/settings.py file.\n\nTo initialize the database, type in the /src/src folder:\n    > python manage.py migration\n\nTo start the sytem on web, type in the /src/src folder:\n    > python manage.py runserver\n\nQuestions\n---------\n\nfeel free to open an `Issue <https://github.com/HallLab/igem/issues>`_.\n\nCiting IGEM\n--------------\n\n\nhttps://igem.readthedocs.io/en/latest/',
    'author': 'Andre Rico',
    'author_email': '97684721+AndreRicoPSU@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.11.0',
}


setup(**setup_kwargs)
