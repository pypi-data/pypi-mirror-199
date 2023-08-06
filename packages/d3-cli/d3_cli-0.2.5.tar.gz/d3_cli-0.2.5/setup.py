# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['d3_scripts']

package_data = \
{'': ['*'],
 'd3_scripts': ['schemas/*', 'theme/static/css/*', 'theme/templates/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'bidict>=0.22.0,<0.23.0',
 'ipython>=8.4.0,<9.0.0',
 'iteration-utilities>=0.11.0,<0.12.0',
 'jsonschema>=4.4.0,<5.0.0',
 'markdown>=3.4.1,<4.0.0',
 'matplotlib>=3.5.2,<4.0.0',
 'networkx>=2.8.3,<3.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pelican-graphviz>=1.2.2,<2.0.0',
 'pelican>=4.8.0,<5.0.0',
 'requests>=2.27.1,<3.0.0',
 'tabulate>=0.9.0,<0.10.0',
 'tqdm>=4.64.0,<5.0.0',
 'yamllint>=1.26.3,<2.0.0']

entry_points = \
{'console_scripts': ['d3-cli = d3_scripts.d3_cli:cli']}

setup_kwargs = {
    'name': 'd3-cli',
    'version': '0.2.5',
    'description': 'Utility scripts for ManySecured-D3 claims',
    'long_description': '# ManySecured d3-cli\n\nUtility cli for ManySecured-D3 claims\n\n## Installation\n\nThis api may be installed using pip like so:\n\n```\npip install d3-cli\n```\n\nWhen developing these scripts, [Python Poetry](https://python-poetry.org/)\nis used to install and manage dependencies as well as publish to [PyPI](https://pypi.org/).\n\nPoetry will create a python isolated virtual environment in the `./.venv` folder and install dependencies if you run:\n\n```bash\npoetry install\n```\n\nYou cannot run the cli or scripts directly from the `./src/d3-scripts` since we are using [Python relative imports](https://realpython.com/absolute-vs-relative-python-imports/#relative-imports).\n\nInstead, you must run the d3-cli script defined in the `[tool.poetry.scripts]` field of [`pyproject.toml`](./pyproject.toml): You can run the command line interface locally, directly from source code without building/installing by running `poetry run d3-cli`.\n\n\n## Usage\n\n```console\nusage: d3-cli [-h] [--version] [--guid] [--output [OUTPUT]] [--mode [{build,lint,export,website}]] [--skip-mal]\n              [--build-dir [BUILD_DIR]] [--check_uri_resolves] [--web-address [WEB_ADDRESS]] [--verbose | --quiet]\n              [input ...]\n\nManySecured D3 CLI for creating, linting and exporting D3 claims\n\npositional arguments:\n  input                 folders containing D3 YAML files.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --version             show the version and exit.\n  --guid, --uuid        generate and show guid and exit.\n  --output [OUTPUT], -o [OUTPUT]\n                        directory in which to output built claims.\n  --mode [{build,lint,export,website}], -m [{build,lint,export,website}]\n                        mode to run d3-cli in.\n                        build creates a directory of D3 claims in json format, with the parent and child types resolved, and CVEvulnerabilities added.\n                        lint lints the claims to check they confirm to the yaml syntax and schemas.\n                        export creates a directory with the CSVs of the tables of types, behaviours andfirmwares.\n                        website creates a directory containing the source for a static website of claims which can be browsed,with unique uris for each type.\n  --skip-mal            skip malicious url lookup.\n                                This takes a bit of time, and requires an internet connection\n                                so you may wish to skip this step for local testing.\n  --build-dir [BUILD_DIR]\n                        build directory with json claims to export to build website with.\n                                Specifying this will skip build step in export mode and website mode.\n  --check_uri_resolves  check that URIs/refs resolve.\n                                This can be very slow, so you may want to leave this off normally.\n  --web-address [WEB_ADDRESS]\n                        web address to use for website build\n  --verbose, -v\n  --quiet, -q\n\nExample: d3-cli ./manufacturers\n```\n\n## Tests\n\nTests can be run via:\n\n```bash\npoetry run pytest\n```\n\n## Publish\n\nThe d3-cli utility is published [here](https://pypi.org/project/d3-cli/).\n\nIn order to publish you must run:\n\n```\npoetry build\npoetry publish\n```\n\nAnd then enter the credentials for the NquiringMinds pypi account.\n\n## D3 type explorer web page\n\nThis static page is generated from (post-processed) D3 statements and [hosted here](https://techworkshub.github.io/ManySecured-D3DB/). This site relies upon two Github actions in the [D3DB repository](https://github.com/TechWorksHub/ManySecured-D3DB)\n- Run D3 Build of website for github pages - processes all files, exporting html files\n- Publish website (main-branch only) deploys the pelecan site to Github pages\n\nIn order for the pelican graphviz plugin which generates the digraph\'s in the webpage to work you need to have graphviz installed on your pc. For linux machines this can be done with `sudo apt install graphviz`, for windows graphviz installers may be downloaded [from here](https://graphviz.org/download/).\n\n\n### Running Locally\n\nTo generate the site files inside a defined directory:\n```\ncd d3-cli\npoetry install\npoetry run d3-cli --mode website "path-to-d3-yaml-files" --output "output-file" \n\n```\n\nserving the static site:\n```\ncd "output-file"/output\npython -m http.server 8000\n```',
    'author': 'NquiringMinds',
    'author_email': 'contact@nquiringminds.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/TechWorksHub/ManySecured-D3DB',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
