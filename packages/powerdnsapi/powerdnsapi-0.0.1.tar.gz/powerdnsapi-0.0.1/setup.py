# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['powerdnsapi']

package_data = \
{'': ['*']}

install_requires = \
['jsonref', 'jsonschema']

setup_kwargs = {
    'name': 'powerdnsapi',
    'version': '0.0.1',
    'description': 'Python PowerDNS API tool for interacting with Authoritative PowerDNS Servers',
    'long_description': '# PowerDNSAPI\n\nPython Package to make API calls to PowerDNS Authoritative Server.\n\nThis does not implement functions for all PowerDNS Authoritative API calls, rather common ones that I want automated.\n\n## Installing\n\nTBD\n\n## Usage\n\n```python\nfrom powerdnsapi import PowerDNSAPI\n\npdns = PowerDNSAPI("http://my_server:8081", "123ABC")\n\npdns.get_servers()\n```\n\n## Q&A\n\n**Why another PowerDNS API python library?** Looking at the existing projects, none suited what I wanted. I wanted to have some helpers to simplify common tasks and also get the data back as a dict/list instead of nested objects.\n\n**Why no tests?** This is a side/after hours project and I haven\'t set aside time for that yet.\n\n## Roadmap\n\n- Add documentation\n- Add PowerDNS Container for local development\n- Add unit tests\n- Add integration tests against different versions of PowerDNS\n',
    'author': 'Nate Gotz',
    'author_email': '775979+nlgotz@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nlgotz/powerdnsapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
