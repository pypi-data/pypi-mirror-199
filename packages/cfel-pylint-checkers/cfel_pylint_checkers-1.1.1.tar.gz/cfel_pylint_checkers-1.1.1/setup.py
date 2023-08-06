# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfel_pylint_checkers']

package_data = \
{'': ['*']}

install_requires = \
['pylint>=2.14.0,<3.0.0']

setup_kwargs = {
    'name': 'cfel-pylint-checkers',
    'version': '1.1.1',
    'description': 'Additional checkers for pylint that are used by the FS-CFEL-1 team',
    'long_description': '# cfel-pylint-checkers\n\n## Installation\n\nJust `pip install cfel-pylint-checkers` should suffice. Then you can enable the appropriate checkers as plugins by editing your `.pylintrc` file, extending the `load-plugins` line. For example:\n\n```\nload-plugins=cfel_pylint_checkers.no_direct_dict_access,cfel_pylint_checkers.tango_command_dtype\n```\n\n## Checkers\n### `no-direct-dict-access`\n\nEnable with:\n\n```\nload-plugins=cfel_pylint_checkers.no_direct_dict_access\n```\n\nThis disallows the use of dictionary access using the `[]` operator *for reading*. Meaning, this is no longer allowed:\n\n```python\nmydict = { "foo": 3 }\n\nprint(mydict["bar"])\n```\n\nAs you can see, this code produces an error, since we’re accessing `"bar"` but the `mydict` dictionary only contains the key `"foo"`. You have to use `.get` to make this safe:\n\n```python\nmydict = { "foo": 3 }\n\nprint(mydict.get("bar"))\n```\n\nWhich produces `None` if the key doesn’t exist. You can even specify a default value:\n\n```python\nmydict = { "foo": 3 }\n\nprint(mydict.get("bar", 0))\n```\n\nMutating use of `operator[]` is, of course, still possible. This is *fine*:\n\n```python\nmydict = { "foo": 3 }\n\nmydict["bar"] = 4\n```\n\n### `tango-command-dtype`\n\nEnable with:\n\n```\nload-plugins=cfel_pylint_checkers.tango_command_dtype\n```\n\nThis checker tests for various error conditions related to the hardware controls system [Tango](https://www.tango-controls.org/), specifically its Python adaptation [PyTango](https://pytango.readthedocs.io/en/stable/). \n\nFor instance, the following mismatch between the `dtype_in` of a command and its actual type annotation is caught:\n\n```python\nfrom tango.server import Device, command\n\nclass MyDevice(Device):\n    @command(dtype_in=int)\n    def mycommand(self, argument: str) -> None:\n        pass\n```\n',
    'author': 'Philipp Middendorf',
    'author_email': 'philipp.middendorf@desy.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.desy.de/cfel-sc-public/cfel-pylint-checkers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
