# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_gcp',
 'django_gcp.events',
 'django_gcp.logging',
 'django_gcp.management',
 'django_gcp.management.commands',
 'django_gcp.metadata',
 'django_gcp.storage',
 'django_gcp.tasks']

package_data = \
{'': ['*'], 'django_gcp': ['static/*', 'templates/django_gcp/*']}

install_requires = \
['Django>=3.0,<5',
 'django-app-settings>=0.7.1,<0.8.0',
 'gcp-pilot>=0.40.0,<0.41.0',
 'google-auth>=2.6.0,<3.0.0',
 'google-cloud-error-reporting>=1.9.0,<2.0.0',
 'google-cloud-pubsub>=2,<3',
 'google-cloud-scheduler>=2,<3',
 'google-cloud-storage>=2.1.0,<3.0.0',
 'google-cloud-tasks>=2,<3',
 'python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'django-gcp',
    'version': '0.8.0',
    'description': 'Utilities to run Django on Google Cloud Platform',
    'long_description': '[![PyPI version](https://badge.fury.io/py/django_gcp.svg)](https://badge.fury.io/py/django_gcp)\n[![codecov](https://codecov.io/gh/octue/django-gcp/branch/main/graph/badge.svg?token=H2QLSCF3DU)](https://codecov.io/gh/octue/django-gcp)\n[![Documentation](https://readthedocs.org/projects/django_gcp/badge/?version=latest)](https://django_gcp.readthedocs.io/en/latest/?badge=latest)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n# DjangoGCP\n\nHelps you to run Django on Google Cloud Platform - Storage, PubSub and Tasks.\n\nRead the [documentation here](https://django_gcp.readthedocs.io/en/latest).\n\nThis app is maintained by Octue - we\'re on a mission to help climate scientists and energy engineers be more efficient. [Find out more](https://www.octue.com).\n\nIf you need some help implementing or updating this, we can help! Raise an issue or [contact us](https://www.octue.com/contact).\n\n## Are you from GCP??\n\nIf so, get in touch for a chat. We\'re doing fun things with Google Cloud. Way funner than boring old django... :)\n\n## All the :heart:\n\nThis app is based heavily on [django-storages](https://django-storages.readthedocs.io/en/latest/), [django-google-cloud-tasks](https://github.com/flamingo-run/django-cloud-tasks) and uses the [django-rabid-armadillo](https://github.com/thclark/django-rabid-armadillo) template. Big love.\n\n## Contributing\n\nIt\'s pretty straightforward to get going, but it\'s good to get in touch first, especially if you\'re planning a big feature.\n\n### Set up\n\nOpen the project in codespaces, a vscode .devcontainer (which is configured out of the box for you) or your favourite IDE or editor (if the latter you\'ll need to set up `docker compose` yourself).\n\nCreate a file `.devcontainer/docker-compose.developer.yml`. This allows you to customise extra services and volumes you make available to the container.\nFor example, you can map your own gcloud config folder into the container to use your own credentials. This example will get you going, but you can just leave the services key empty.\n\n```\nversion: "3.8"\n\nservices:\n  web:\n    volumes:\n      - ..:/workspace:cached\n      - $HOME/.config/gcloud:/gcp/config\n\n    environment:\n      - CLOUDSDK_CONFIG=/gcp/config\n      - GOOGLE_APPLICATION_CREDENTIALS=/gcp/config/your-credentials-file.json\n```\n\n### Initialise gcloud CLI\n\nTo sign in (enabling use of the gcloud CLI tool), do:\n\n```\ngcloud config set project octue-django-gcp\ngcloud auth login\n```\n\n### Run the tests\n\nRun the tests:\n\n```\npytest .\n```\n\nWe use pre-commit to ensure code quality standards (and to help us automate releases using conventional-commits). If you can get on board with this that\'s really helpful - if not, don\'t fret, we can help.\n\n### Use the example app\n\nYou can start the example app (which is useful for seeing how `django-gcp` looks in the admin.\n\nInitially, do:\n\n```\npython manage.py migrate\npython manage.py createsuperuser\n# make yourself a user account at the prompt\n```\n\nThen to run the app, do:\n\n```\npython manage.py runserver\n```\n\n...and visit [http://localhost:8000/admin/](http://localhost:8000/admin/) to sign in.\n\n### Update the docs\n\nWe\'re pretty good on keeping the docs helpful, friendly and up to date. Any contributions should be\nfully documented.\n\nTo help develop the docs quickly, we set up a watcher that rebuilds the docs on save. Start it with:\n\n```\npython docs/watch.py\n```\n\nOnce docs are building, the the vscode live server extension (or whatever the equivalent is in your IDE)\nto live-reload `docs/html/index.html` in your browser, then get started!\n',
    'author': 'Tom Clark',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/octue/django-gcp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
