# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metadeco']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.5.0,<5.0.0']

setup_kwargs = {
    'name': 'metadeco',
    'version': '0.2.1',
    'description': 'Metadeco allows you to set metadata to decorated objects.',
    'long_description': '# Metadeco\n\nMetadata reflections for functions/methods. Inspired by NPM\'s [`reflect-metadata`](https://www.npmjs.com/package/reflect-metadata) package.\n\n## How to use:\n\n### To decorate a function:\n\n```py\nimport metadeco\n\n# Define a function with the "__has_print__" metadata set to "True"\n# You can set anything has the value of the metadata.\n@metadeco.metadata("__has_print__", True)\ndef my_function():\n    print("Hello world!")\n\nmetadeco.has_metadata(my_function)\n# We would get "True"\n\nmetadeco.get_metadata(my_function, "__has_print__")\n# We obtain the value set by the function, in here, "True\nmetadeco.get_metadata(my_function, "__not_set__")\n# "NoMetadataError" is raised here.\n\nmetadeco.delete_metadata(my_function, "__has_print__")\n# Delete the metadata.\n```\n\n## To decorate a property:\n\n```py\nimport metadeco\n\n\nclass MySettings:\n    \n    @metadeco.decorate("__output__", "Hey there!")\n    def test():\n        return "Hey there!"\n\n# Getting the metadata of "test" property in object MySettings\nmetadeco.get_metadata(MySettings, "__output__", "test")\n# We get "Hey there"\n```\n',
    'author': 'Predeactor',
    'author_email': 'pro.julien.mauroy@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
