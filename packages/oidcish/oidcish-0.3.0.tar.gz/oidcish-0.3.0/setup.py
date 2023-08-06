# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['oidcish', 'oidcish.flows']

package_data = \
{'': ['*']}

install_requires = \
['StrEnum>=0.4.9,<0.5.0',
 'background>=0.2.1,<0.3.0',
 'beautifulsoup4>=4.11.2,<5.0.0',
 'cryptography>=38.0.4,<39.0.0',
 'httpx>=0.23.3,<0.24.0',
 'pendulum>=2.1.2,<3.0.0',
 'pkce>=1.0.3,<2.0.0',
 'pydantic>=1.10.5,<2.0.0',
 'python-dotenv>=0.21.1,<0.22.0',
 'python-jose>=3.3.0,<4.0.0']

setup_kwargs = {
    'name': 'oidcish',
    'version': '0.3.0',
    'description': 'Obtain authentication tokens from OIDC providers.',
    'long_description': '# oidcish\n\n- "Oh I Don\'t Care If Something Happens"\n- "OIDC Is Definitely Cool If Someone Helps"\n\n## What?\n\nLibrary to connect to your OIDC provider via:\n\n- Authentication code flow\n- Device code flow\n\n## Usage\n\n```python\n>>> from oidcish import DeviceFlow, CodeFlow, CredentialsFlow\n>>> auth = DeviceFlow(\n...     host="https://idp.example.com",\n...     client_id=...,\n...     client_secret=...,\n...     scope=...,\n...     audience=...\n...)\nVisit https://idp.example.com/device?userCode=594658190 to complete sign-in.\n# Or use env file for auth\n# auth = DeviceFlow(_env_file="path/to/my/env.file")\n# Or use authorization code flow\n# auth = CodeFlow(_env_file="path/to/my/env.file")\n# Or use client credentials flow\n# auth = CredentialsFlow(_env_file="path/to/my/env.file")\n>>> print(auth.credentials.access_token)\neyJhbGciOiJSU...\n```\n\n## Options\n\nDevice flow can be used with the following options:\n\n| Option | Environment variable | Default | Description |\n|-|-|-|-|\n| host | OIDCISH_HOST | *No default* | The address to the IDP server. |\n| client_id | OIDCISH_CLIENT_ID | *No default* | The client id. |\n| client_secret | OIDCISH_CLIENT_SECRET | *No default* | The client secret. |\n| scope | OIDCISH_SCOPE | openid profile offline_access | A space separated, case-sensitive list of scopes. |\n| audience | OIDCISH_AUDIENCE | *No default* | The access claim was designated for this audience. |\n\nThe OIDCISH_ prefix can be set with the OIDCISH_ENV_PREFIX environment variable.\n\nCode flow can be used with the following options:\n\n| Option | Environment variable | Default | Description |\n|-|-|-|-|\n| host | OIDCISH_HOST | *No default* | The address to the IDP server. |\n| client_id | OIDCISH_CLIENT_ID | *No default* | The client id. |\n| client_secret | OIDCISH_CLIENT_SECRET | *No default* | The client secret. |\n| redirect_uri | OIDCISH_REDIRECT_URI | http://localhost | Must exactly match one of the allowed redirect URIs for the client. |\n| username | OIDCISH_USERNAME | *No default* | The user name. |\n| password | OIDCISH_PASSWORD | *No default* | The user password. |\n| scope | OIDCISH_SCOPE | openid profile offline_access | A space separated, case-sensitive list of scopes. |\n| audience | OIDCISH_AUDIENCE | *No default* | The access claim was designated for this audience. |\n\nThe OIDCISH_ prefix can be set with the OIDCISH_ENV_PREFIX environment variable.\n\nClient credentials flow can be used with the following options:\n\n| Option | Environment variable | Default | Description |\n|-|-|-|-|\n| host | OIDCISH_HOST | *No default* | The address to the IDP server. |\n| client_id | OIDCISH_CLIENT_ID | *No default* | The client id. |\n| client_secret | OIDCISH_CLIENT_SECRET | *No default* | The client secret. |\n| audience | OIDCISH_AUDIENCE | *No default* | The access claim was designated for this audience. |\n\nThe OIDCISH_ prefix can be set with the OIDCISH_ENV_PREFIX environment variable.\n',
    'author': 'Erik G. Brandt',
    'author_email': 'erik.brandt@shaarpec.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
