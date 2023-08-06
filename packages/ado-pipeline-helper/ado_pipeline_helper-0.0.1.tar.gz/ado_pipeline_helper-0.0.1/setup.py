# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ado_pipeline_helper', 'ado_pipeline_helper.resolver']

package_data = \
{'': ['*']}

install_requires = \
['azure-devops>=6.0.0b4,<7.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'pyright>=1.1.298,<2.0.0',
 'ruamel-yaml>=0.17.21,<0.18.0',
 'structlog>=22.3.0,<23.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['ado-pipeline-helper = ado_pipeline_helper.cli:cli']}

setup_kwargs = {
    'name': 'ado-pipeline-helper',
    'version': '0.0.1',
    'description': '',
    'long_description': "# ADO Pipeline helper \n\nPython package and commandline tool for helping with writing Azure Devops pipelines.\n\n# Features\nNone of these are implemented mind you as of now\n\n- validate pipeline (load .azure-pipeline, resolve templates, send to run endpoint with yamlOverride and preview=True)\n- validate library groups (see if value exists)\n- MAYBE: validate schedule cron\n- Warning about templating syntax errors (like missing $ before {{ }} )\n\n## Limitations\n\n- Can't resolve `{{ }}` expressions, only simple `{{ parameter.<key>}}` ones.\nI started working on a custom resovler but it was a lot of work. You can see it on the branch `expression resolver` under\n`ado_pipeline_helper/src/ado_pipeline_helper/resolver/expression.py`\n\n## Useful links\n\n- [ADO Yaml Reference](https://learn.microsoft.com/en-us/azure/devops/pipelines/yaml-schema/?view=azure-pipelines)\n\n",
    'author': 'StefanBRas',
    'author_email': 'gitcommits@bruhn.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
