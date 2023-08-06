# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlite_dataset']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy>=2.0,<3.0']

setup_kwargs = {
    'name': 'sqlite-dataset',
    'version': '0.1.0',
    'description': 'Use SQLite database to store datasets.',
    'long_description': "# SQLite Dataset\n\nUse [SQLite](https://sqlite.org/index.html) database to store datasets. Based on [SQLAlchemy core](https://docs.sqlalchemy.org/en/20/core/).\n\n## Structure\n\nThe core of sqlite-dataset is the Class **SQLiteDataset**, which wraps a SQLAlchemy connection to a SQLite database.\n\n## Usage\n\n### Create a new dataset\n\nA **schema** is required to create a new dataset. The **schema** should be a dictionary where each item is a column.\n\nThere are two ways to specify the schema:\n\n1. Extend the base **SQLiteDataset** class and override the **schema** field.\n\n```python\nfrom sqlite_dataset import SQLiteDataset\nfrom sqlalchemy import Column, String, Float\n\nclass MyIrisDataset(SQLiteDataset):\n    schema = {\n        'iris': [\n            Column('sepal_length_cm', String),\n            Column('sepal_width_cm', Float),\n            Column('petal_length_cm', Float),\n            Column('petal_width_cm', Float),\n            Column('class', String),\n        ]\n    }\n\nds = MyIrisDataset.create('test.db')\n```\n\n2. Pass schema to `SQLiteDataset.create()`\n\n```python\nschema = {\n    'iris': [\n        Column('sepal_length_cm', String),\n        Column('sepal_width_cm', Float),\n        Column('petal_length_cm', Float),\n        Column('petal_width_cm', Float),\n        Column('class', String),\n    ]\n}\nds = SQLiteDataset.create('test.db', schema=schema)\n```\n\nBe aware that the schema passed to `SQLiteDataset.create()` will override the class field schema.\n\n### Connect to an existing dataset\n\nAn existing dataset could be one created by calling `SQLiteDataset.create()` as shown above, or could be any SQLite database file.\n\nTo connect to a dataset, call the `connect()` method and `close()` after complete all tasks.\n\n```python\nds = SQLiteDataset('test.db')\nds.connect()\n# do something\nds.close()\n```\n\nOr the dataset can be used as a context manager\n\n```python\nwith SQLiteDataset('test.db') as ds:\n    # do something\n    pass\n```\n\n### Schema for existing dataset\n\n**SQLiteDataset** object uses SQLAlchemy connection under the hood, soa schema is required to make any database queries or operations.\n\nThe way to specify schema for an existing dataset is similar to *create a new dataset*.\n\nIf it's a class extending the base SQLiteDataset class, and overrides the schema field, then this schema will be used.\n\n```python\nwith MyIrisDataset('test.db') as ds:\n    pass\n```\n\nOr a schema can be passed into the class constructor. The schema passed into the constructor will always override the class field schema.\n\n```python\nwith MyIrisDataset('test.db', schema=schema) as ds:\n    pass\n\nwith SQLiteDataset('test.db', schema=schema) as ds:\n    pass\n```\n\nIf no schema provided by either of the above, a [SQLAlchemy **reflection**](https://docs.sqlalchemy.org/en/13/core/reflection.html) is performed to load and parse schema from the existing database.\n\n```python\nwith SQLiteDataset('test.db') as ds:\n    pass\n```\n\nIt is recommended to explicitly define the schema as **reflection** may have performance issue in some cases if the schema is very large and complex.\n\n## Add and read data\n\n```python\ndata = [\n    {\n        'sepal_length_cm': '5.1',\n        'sepal_width_cm': '3.5',\n        'petal_length_cm': '1.4',\n        'petal_width_cm': '0.2',\n        'class': 'setosa'\n    },\n    {\n        'sepal_length_cm': '4.9',\n        'sepal_width_cm': '3.0',\n        'petal_length_cm': '1.4',\n        'petal_width_cm': '0.2',\n        'class': 'setosa'\n    }\n]\n\nwith MyIrisDataset('test.db') as ds:\n    ds.insert_data('iris', data)\n```\n\n```python\nwith MyIrisDataset('test.db') as ds:\n    res = ds.read_data('iris')\n```\n\n\n### Use with pandas\n\nA pandas DataFrame can be inserted into a dataset by utilizing the `to_sql()` function, and read from the dataset using `read_sql` function.\n\nBe aware that in this case, `SQLiteDataset()` should be used without specifying the schema.\n\n```python\nimport seaborn as sns\nimport pandas as pd\n\ndf = sns.load_dataset('iris')\nwith SQLiteDataset('iris11.db') as ds:\n    df.to_sql('iris', ds.connection)\n    ds.connection.commit()\n```\n\n```python\nwith SQLiteDataset('iris11.db') as ds:\n    res = pd.read_sql(\n        ds.get_table('iris').select(),\n        ds.connection\n    )\n```",
    'author': 'Jinshuai Ma',
    'author_email': 'mayazureee@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
