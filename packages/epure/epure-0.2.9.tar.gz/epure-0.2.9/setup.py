# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['epure',
 'epure.helpers',
 'epure.parser',
 'epure.resource',
 'epure.resource.db',
 'epure.resource.file',
 'epure.resource.gres',
 'epure.resource.lite_db',
 'epure.resource.node']

package_data = \
{'': ['*']}

install_requires = \
['inflection>=0.5.1,<0.6.0',
 'jsonpickle>=2.2.0,<3.0.0',
 'psycopg2==2.9.3',
 'twine>=4.0.2,<5.0.0']

setup_kwargs = {
    'name': 'epure',
    'version': '0.2.9',
    'description': 'purest architecture',
    'long_description': 'Epure\n=====\n\n<a href="https://github.com/nagvalhm/epure">Epure</a> is agnostic ORM - you can store and retrieve data having no idea about database, table and columns. \nAll technical details hidden from you. Care only about your business logic.\n\n\nInstalling\n----------\n\nInstall and update using <a href="https://pip.pypa.io/en/stable/getting-started/">`pip`</a>:\n\n```\n    $ pip install -U epure\n```\n\nInstall and update using <a href="https://python-poetry.org/docs/">`poetry`</a>:\n\n```\n    $ poetry add epure\n```\n\n\nConnecting Epure to database\n----------\n\nCreate example class with Epure, create instance of it and read it from DB.\n\n```python\n\n    # import connection functions from Epure\n    from epure import GresDb\n    from epure import connect\n\n    # First way to connect database to epure\n\n    # Format of string to connect (\'database://user:password@host:port\')\n    GresDb(\'postgres://postgres:postgres@localhost:5432\',\n    log_level=3).connect()\n\n    # Alternative way of connection\n\n    db = GresDb(\'postgres://postgres:postgres@localhost:32\', \n    # host="localhost", \n    port="5432", \n    # database="postgres", \n    # user="postgres", \n    password="postgres",\n    log_level=3)\n    db.connect()\n\n    # log_level defines level of description of opertaions with DB in auto-generated file epure_db.log\n\n```\n\n\nA Simple Example\n----------------\n\n```python\n\n    # save this as epure_example.py\n    from epure import epure\n\n    # different types hints avalible\n    import types\n\n    # In order to save attributes of class to db, type hints is required!\n\n    # decorate class by @epure() wrap function\n    @epure()\n    class Example:\n\n        int_attr:int\n        bool_attr:bool\n        str_attr:str\n        complex_attr:complex\n        list_attr:list\n        dict_attr:Dict[int, str]\n        str_attr_with_default_val:str = \'example_str\'\n        epure_cls_attr:SomeEpureCls\n        NoneType_attr:types.NoneType\n\n    # creating instance of epurized Example class\n    obj = Example()\n    \n    # assigning vals to instance\n    obj.int_attr = 1\n    obj.str_attr = "example"\n    obj.list_attr = [1,2,3,4]\n\n    #saving obj instance to database\n    obj.save()\n\n    # saved instance has attribute of node_id that is unique\n    node_id = epure.node_id \n    \n    # node_id is used to search epure objects and retrive them from DB via read() method\n    res = epure.table.read(node_id=node_id)\n\n```\n\nDevelopers\n-----\nNikita Umarov (Pichugin), \nPavel Pichugin\n\n\nLinks\n-----\n\n-   Documentation: https://github.com/nagvalhm/epure/blob/main/README.md\n-   Changes: https://github.com/nagvalhm/epure\n-   PyPI Releases: https://pypi.org/project/epure/\n-   Source Code: https://github.com/nagvalhm/epure\n-   Issue Tracker: https://github.com/nagvalhm/epure/issues\n-   Website: https://pypi.org/project/epure/',
    'author': 'Nikita Umarov',
    'author_email': 'nagvalhm@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
