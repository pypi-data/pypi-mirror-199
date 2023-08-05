# SQL Translator

About A lib to translate natural language to sql

[![Github Issues](http://img.shields.io/github/issues/hudsonbrendon/sql-translator.svg?style=flat)](https://github.com/hudsonbrendon/sql-translator/issues?sort=updated&state=open)
![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)

# Recursos Disponíveis

- [x] Transcribe natural language to sql
- [ ] Transcribe sql to natural language

# Instalação

```bash
$ pip install sql-translator
```

or

```bash
$ poetry build
```

# Usage

```python
from sql_translator import Sql

sql = Sql(<open_ia_api_key>)

sql.translator("return all products")
```

## Result:

```SQL
SELECT * ALL PRODUCTS
```

# contribute

Clone the project repository:

```bash
$ git clone https://github.com/hudsonbrendon/sql-translator.git
```

Make sure [Poetry](https://python-poetry.org/) is installed, otherwise:

```bash
$ pip install -U poetry
```

Install dependencies:

```bash
$ poetry install
```

```bash
$ poetry shell
```

Run tests:

```bash
$ pytest
```

# Dependencies

- [Python >=3.10](https://www.python.org/downloads/release/python-3813/)

# License

[MIT](http://en.wikipedia.org/wiki/MIT_License)
