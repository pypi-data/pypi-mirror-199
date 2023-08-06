# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['freak']

package_data = \
{'': ['*']}

install_requires = \
['fastapi', 'uvicorn']

setup_kwargs = {
    'name': 'freak',
    'version': '0.0.1',
    'description': 'Remote application state control',
    'long_description': '# Freak\n\nControl.\n\nControl your application state with a single line of code.\n\nFreak is using `pydantic` to define the state, supports nested models, partial updates, data validation, and uses `FastAPI` to serve the state over HTTP.\n\n## Installation\n```shell\npip install freak\n```\n\n## Usage\n\nDefine a `pydantic` model and pass it to the `control` function.\n\n```python\nfrom freak import control\nfrom pydantic import BaseModel\n\nclass State(BaseModel):\n    foo: str = "bar"\n\nstate = State()\ncontrol(state)\n```\n\nThe `state` object will now be automatically served over HTTP.\n\nFreak generates `/get/<field>` and `/set/<field>` endpoints for each field in the model, as well as the following endpoints for the root state object:\n - `/get` (`GET`)\n - `/set` (`PATCH`)\n - `/reset` (`DELETE`)\n - `/get_from_path` (`GET`) - which allows to get a value from the state using dot-notation (like `my.inner.field.`)\n\nThe `foo` field can now be modified externally by sending a PUT request to the Freak server, which has been automatically started in the background:\n\n```shell\ncurl -X PUT localhost:4444/set/foo?value=baz\n```\n\nAt the same time, the `state` object cat be used in the program. Freak will always modify it in place. This can be helpful for long-running programs that need to be controlled externally, like:\n - training a neural network\n - running a bot\n - etc.\n\nFreak supports nested models and partial updates. Consider the following model:\n\n```python\nfrom pydantic import BaseModel\n\nclass Bar(BaseModel):\n    foo: str = "bar"\n    baz: str = "qux"\n\nclass State(BaseModel):\n    bar: Bar = Bar()\n```\n\nFreak will generate `put` endpoints for the `foo` and `baz` fields, and a `patch` endpoint for the `bar` field (as it\'s a `pydantic` model itself). This `patch` endpoint supports partial updates:\n\n```shell\ncurl -X PATCH localhost:4444/set/bar -d \'{"foo": "baz"}\'\n```\n\nBecause Freak is using `FastAPI`, it\'s possible to use auto-generated documentation to interact with the Freak server. The interactive documentation can be accessed at Freak\'s main endpoint, which by default is `localhost:4444`.\n\nThe following screenshot shows the generated endpoints for the DL [example](https://github.com/danielgafni/freak/blob/master/examples/dl_example.py):\n\n![Sample Generated Docs](https://raw.githubusercontent.com/danielgafni/freak/master/resources/swagger.png)\n\n## Development\n\n### Installation\n\n```shell\npoetry install\npoetry run pre-commit install\n```\n### Testing\n\n```shell\npoetry run pytest\n```\n',
    'author': 'Daniel Gafni',
    'author_email': 'danielgafni16@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/danielgafni/freak',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
