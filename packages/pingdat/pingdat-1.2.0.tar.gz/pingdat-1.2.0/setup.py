# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pingdat']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'ping3>=4.0.4,<5.0.0',
 'prometheus-client>=0.16.0,<0.17.0',
 'pydantic>=1.10.7,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.2,<3.0.0']

entry_points = \
{'console_scripts': ['pingdat = pingdat.__main__:main']}

setup_kwargs = {
    'name': 'pingdat',
    'version': '1.2.0',
    'description': 'A simple ping exporter for Prometheus metrics.',
    'long_description': '# pingdat #\n\n[![PyPI](https://img.shields.io/pypi/v/pingdat.svg)](https://pypi.org/project/pingdat)\n[![LICENSE](https://img.shields.io/github/license/jheddings/pingdat)](LICENSE)\n[![Style](https://img.shields.io/badge/style-black-black)](https://github.com/ambv/black)\n\nA Prometheus exporter for ping statistics.\n\n## Installation ##\n\nInstall the published package using pip:\n\n```shell\npip3 install pingdat\n```\n\nThis project uses `poetry` to manage dependencies and a local virtual environment.  To\nget started, clone the repository and install the dependencies with the following:\n\n```shell\npoetry install\n```\n\n### Grafana Dashboard ###\n\nA Grafana dashboard is available as #(17922)[https://grafana.com/grafana/dashboards/17922].\n\n## Usage ##\n\nRun the module and tell it which config file to use.\n\n```shell\npython3 -m pingdat --config pingdat.yaml\n```\n\nIf you are using `poetry` to manage the virtual environment, use the following:\n\n```shell\npoetry run pingdat --config pingdat.yaml\n```\n\n### Docker ###\n\n`pingdat` is available as a published Docker image.  To run, use the latest version:\nfrom Docker Hub:\n\n```shell\ndocker container run --rm --publish 9056:9056 "jheddings/pingdat:latest"\n```\n\nThe configuration file is read from `/opt/pingdat/pingdat.yaml` and may be changed\nwith arguments to the container:\n\n```shell\ndocker container run --rm --tty --publish 9056:9056 \\\n  --volume "/path/to/host/config:/etc/pingdat" \\\n  "jheddings/pingdat:latest" --config /etc/pingdat/pingdat.yaml\n```\n\n## Docker Compose ##\n\nA sample configuration is also provided for using `docker compose`.  Similar to using\nDocker directly, the configuration file can be provided on the host side.  Then,\nsimply start the cluster normally:\n\n```shell\ndocker compose up\n```\n\nOr detached as a background process:\n\n```shell\ndocker compose up --detach\n```\n\n## Configuration ##\n\nFor now, review the sample `pingdat.yaml` config file for a description of supported\nconfiguration options.\n',
    'author': 'jheddings',
    'author_email': 'jheddings@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
