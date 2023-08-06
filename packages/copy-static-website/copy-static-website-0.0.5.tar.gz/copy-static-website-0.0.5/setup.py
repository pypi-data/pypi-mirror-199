# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['copy_static_website',
 'copy_static_website.deploy.ftp',
 'copy_static_website.download',
 'copy_static_website.update_site_ftp',
 'copy_static_website.utils']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.2,<5.0.0',
 'ftputil>=5.0.4,<6.0.0',
 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'copy-static-website',
    'version': '0.0.5',
    'description': 'A hopefully simple tool to copy a static website, with all local resources included.',
    'long_description': "# Copy a static website easily\n\nThis tool will help you by downloading a static website, together with all it's local resources.\n\nThis project is in its early development stages, so avoid it for production environments.\n\nFeel free to report issues and send pull requests.\n",
    'author': 'Federico Giancarelli',
    'author_email': 'hello@federicogiancarelli.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
