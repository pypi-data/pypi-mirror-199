# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nautikos']

package_data = \
{'': ['*']}

install_requires = \
['ruamel-yaml>=0.17.21,<0.18.0', 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['nautikos = nautikos.cli:app']}

setup_kwargs = {
    'name': 'nautikos',
    'version': '0.2.3',
    'description': 'A CD tool for updating image tags in Kubernetes manifests',
    'long_description': "# Nautikos \n\n*A lightweight CI/CD tool for updating image tags in Kubernetes manifests.* \n\n[![PyPI version](https://badge.fury.io/py/nautikos.svg)](https://badge.fury.io/py/nautikos)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Python versions](https://img.shields.io/pypi/pyversions/nautikos)]()\n\n## Rationale\n\nA GitOps CI/CD process usually uses a deployment or ops repo containing Kubernetes manifests for multiple services and environments. Tools like *Argo-CD* or *Flux* then track these repo's, and apply any changes to the cluster. When a new image of an application is created, you want the corresponding tags to be updated in the manifests. Doing this manually is error prone. Having to write logic in every repo or pipeline to perform this is tedious. \n\nThis is where Nautikos comes in. \n\n## Installation \n\n```bash\npip install nautikos\n```\n\n## Basic usage \n\nNautikos is configured through a YAML-file (`./nautikos.yaml`), that specifies where the manifests for the different images and environments can be found: \n\n```yaml\nenvironments: \n- name: prod \n  manifests: \n  - path: prod/app1/deployment.yaml  # Path relative to configuration file\n    type: kubernetes  # Type can be 'kubernetes' or 'kustomize'\n    labels:  # Optional specification of labels for more granular control\n    - app1\n    - refs/heads/main\n  - path: prod/app2/kustomize.yaml\n    type: kustomize\n- name: dev\n  manifests: \n  - path: dev/app1/deployment.yaml\n    type: kubernetes\n    labels: \n    - app1\n    - refs/heads/dev\n  - path: dev/app3/feature-A/deployment.yaml\n    type: kubernetes\n    labels: \n    - app1\n    - refs/heads/feature-A\n```\n\nNext, you can run Nautikos to update the image tags of specific images in different environments.\n\n```bash\nnautikos my-repo 1.2.3  # Updates all occurences of `my-repo` to `1.2.3` in all manifests\nnautikos --env prod my-repo 2.3.4  # Updates all occurences of `my-repo` to `2.3.4` in `prod/app1/deployment.yaml` and `prod/app2/deployment`\nnautikos --env dev --labels app1 my-repo 4.5.6  # Updates all occurences of `my-repo` to `4.5.6` in `dev/app1/deployment.yaml`\nnautikos --labels 'app1,refs/heads/main' my-repo 5.6.7  # Updates all occurences of `my-repo` to `5.6.7` in `prod/app1/deployment.yaml`\n```\n\n## Supported tools\n\nThe tool works with standard **Kubernetes** manifests and **Kustomize** - **Helm** might be added later. Each have their own format for defining image tags. \n\n```yaml\n# Kubernetes manifests\nspec:\n  template:\n    spec:\n      containers:\n      - image: some-repository:tag\n\n# Kustomize\nimages: \n- name: some-repository\n  newTag: tag \n```\n\n## Advanced usage\n\nNautikos takes several options: \n\n* `--dry-run`: prints the modified files to stdout, but doesn't edit in place \n* `--config config-file.yaml`: path to config YAML, default is `./nautikos.yaml`\n\n## Alternatives \n\nThere are basically three alternatives to do the same thing: \n\n* **Update manifests manually** - of course this works, but this is not really proper CD\n* **Write your own bash scripts in a pipeline using a tool like `sed` or `yq`** - This works, but having to write this logic for every project is tedious. \n* **Use a tool like [Argo-CD Image updater](https://argocd-image-updater.readthedocs.io/en/stable/)** - very nice, but a bit heavy-weight, not very actively developed, and doesn't seem to support Azure Container Registry. \n\n## Notes \n\nMultiple YAML docs in one file is not yet supported. \n\n## Dependencies \n\n* **`typer`** - for creating a CLI \n* **`ruamel.yaml`** - for handling YAML files while maintaining ordering and comments\n",
    'author': 'Jan Hein de Jong',
    'author_email': 'janhein.dejong@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
