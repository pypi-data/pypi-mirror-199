# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mongorm']

package_data = \
{'': ['*']}

install_requires = \
['motor>=3.1.1,<4.0.0', 'pydantic>=1.10.5,<2.0.0']

setup_kwargs = {
    'name': 'python-mongorm',
    'version': '0.1.0',
    'description': 'MongORM is an ORM (object relational mapping) wrapper using async library motor for MongoDB connection and pydantic for data definition and validation.',
    'long_description': '# MongORM\n\n![MongORM](./banner.png)\n\n`MongORM` is an ORM (object relational mapping) wrapper using async library motor for `MongoDB` connection and pydantic for data definition and validation.\n\n**This module is a work in progress and API may change radically.**\n\n`MongORM` uses [`pydantic`](https://docs.pydantic.dev/) for data validation\nand [`motor`](https://www.mongodb.com/docs/drivers/motor/) for async MongoDB connection.\n\n## Installation\n\nUsing PIP:\n\n```console\npip install python-mongorm\n```\n\nUsing poetry:\n\n```console\npoetry add python-mongorm\n```\n\n## Usage\n\n### Create client\n\n```python\nfrom mongorm import MongORM\n\nclient = MongORM("mongodb://root:root@localhost:27017/", "database")\n```\n\n### Define model\n\n```python\nfrom mongorm import BaseModel, MongoIndex, MongoIndexType\n\nclass Book(BaseModel):\n    """Define models the way you would define pydantic models"""\n\n    class Meta:\n        """Meta contains the model\'s configuration and indexes"""\n        client = client  # pass the client to the model\'s Meta\n        collection = "books"\n        title = MongoIndex("title", MongoIndexType.ASCENDING)\n        author = MongoIndex("author", MongoIndexType.ASCENDING)\n    \n    # id field of type ObjectId is created automatically\n    title: str\n    author: str\n    year_published: int\n\n```\n',
    'author': 'Tomas Votava',
    'author_email': 'info@tomasvotava.eu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tomasvotava/mongorm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
