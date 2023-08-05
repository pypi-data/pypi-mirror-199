# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sql_translator']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'sql-translator',
    'version': '0.1.0',
    'description': 'About A lib to translate natural language to sql',
    'long_description': '# SQL Translator\n\nAbout A lib to translate natural language to sql\n\n[![Github Issues](http://img.shields.io/github/issues/hudsonbrendon/sql-translator.svg?style=flat)](https://github.com/hudsonbrendon/sql-translator/issues?sort=updated&state=open)\n![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)\n\n# Recursos Disponíveis\n\n- [x] Transcribe natural language to sql\n- [ ] Transcribe sql to natural language\n\n# Instalação\n\n```bash\n$ pip install sql-translator\n```\n\nor\n\n```bash\n$ poetry build\n```\n\n# Usage\n\n```python\nfrom sql_translator import Sql\n\nsql = Sql(<open_ia_api_key>)\n\nsql.translator("return all products")\n```\n\n## Result:\n\n```SQL\nSELECT * ALL PRODUCTS\n```\n\n# contribute\n\nClone the project repository:\n\n```bash\n$ git clone https://github.com/hudsonbrendon/sql-translator.git\n```\n\nMake sure [Poetry](https://python-poetry.org/) is installed, otherwise:\n\n```bash\n$ pip install -U poetry\n```\n\nInstall dependencies:\n\n```bash\n$ poetry install\n```\n\n```bash\n$ poetry shell\n```\n\nRun tests:\n\n```bash\n$ pytest\n```\n\n# Dependencies\n\n- [Python >=3.10](https://www.python.org/downloads/release/python-3813/)\n\n# License\n\n[MIT](http://en.wikipedia.org/wiki/MIT_License)\n',
    'author': 'Hudson Brendon',
    'author_email': 'contato.hudsonbrendon@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
