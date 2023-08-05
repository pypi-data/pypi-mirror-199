# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_client_generator', 'python_client_generator.templates']

package_data = \
{'': ['*']}

install_requires = \
['chevron>=0.14.0,<0.15.0', 'pydantic>=1.9.1,<2.0.0']

entry_points = \
{'console_scripts': ['poetry = poetry.console:main']}

setup_kwargs = {
    'name': 'python-client-generator',
    'version': '1.0.4',
    'description': 'Python package to generate an httpx-based client off an OpenAPI spec',
    'long_description': '# python-client-generator\n\nPython package to generate an [httpx](https://github.com/encode/httpx)- and\n[pydantic](https://github.com/pydantic/pydantic)-based async (or sync) \nclient off an OpenAPI spec.\n\n```mermaid\nflowchart LR\n    generator["python-client-generator"]\n    app["REST API app"]\n    package["app HTTP client"]\n\n    app -- "OpenAPI json" --> generator\n    generator -- "generates" --> package\n```\n\n\n## Using the generator\n\n```bash\npython -m python_client_generator --open-api openapi.json --package-name foo_bar --project-name foo-bar --outdir clients\n```\n\nThis will produce a Python package with the following structure:\n```bash\nclients\n├── foo_bar\n│\xa0\xa0 ├── __init__.py\n│\xa0\xa0 ├── apis.py\n│\xa0\xa0 ├── base_client.py\n│\xa0\xa0 └── models.py\n└── pyproject.toml\n```\n\n### Using PATCH functions from the generator\n\nWhen calling one of the generated update functions that uses an HTTP `PATCH` method, you\'ll\nprobably want to pass the additional argument `body_serializer_args={"exclude_unset": True}`. This\nwill ensure that only the fields that are set in the update object are sent to the API. Example:\n\n```python\nawait api_client.update_contact_v1_contacts__contact_id__patch(\n                body=patch_body,\n                contact_id=contact.id,\n                tenant=tenant,\n                body_serializer_args={"exclude_unset": True}\n)\n```\n\n\n## Contributing\nInstall the dependencies with `poetry`:\n```shell\npoetry install\n```\n\nFormat the code:\n```shell\nmake format\n```\n\nTest the code locally:\n```shell\npoetry run pytest\n```\n\n\n### Commiting\n\nWe use commitlint in the CI/CD to make sure all commit messages adhere to [conventionalcommits](https://www.conventionalcommits.org/en/v1.0.0/). See `.commitlintrc.js`, `.releaserc` and `.czrc.json` for specific implementation details.\n\nAs per the default commitlint settings for conventionalcommits ([see here](https://github.com/conventional-changelog/commitlint))\nthe following commit types may be used:\n\n  - `build`\n  - `chore`\n  - `ci`\n  - `docs`\n  - `feat`\n  - `fix`\n  - `perf`\n  - `refactor`\n  - `revert`\n  - `style`\n  - `test`\n\nOf which the following will cause a release (one of these types *must* be used if you are submitting code\nthat you expect to be deployed after merging):\n\n  - `build`\n  - `ci`\n  - `docs(api)`\n  - `feat`\n  - `fix`\n  - `perf`\n  - `refactor`\n  - `revert`\n  \nTo ensure that your commits always conform to the above format, you can install `commitizen`:\n```shell\nnpm i -g commitizen\n```\n',
    'author': 'Trevor Pace',
    'author_email': 'trevor.pace@sennder.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
