# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nautikos']

package_data = \
{'': ['*']}

install_requires = \
['ruamel-yaml>=0.17.21,<0.18.0', 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['nautikos = nautikos.nautikos:app']}

setup_kwargs = {
    'name': 'nautikos',
    'version': '0.1.0',
    'description': 'A CD tool for updating image tags in Kubernetes manifests',
    'long_description': "# Nautikos \n\nNautikos is a CLI tool for updating image tags in Kubernetes manifests, as part of a GitOps CI/CD process. \n\n## Rationale\n\nIn a GitOps CI/CD process, a deployment repo contains Kubernetes manifests for multiple services and environments, that are tracked by a tool like *Argo-CD* or *Flux*. When a new image of an application is created, you want the tags for that image to be updated in the manifests. Doing this manually is error prone. Having to write logic in every repo or pipeline to perform this is tedious. \n\nThis is where Nautikos comes in. \n\n## Installation \n\n```bash\npip install nautikos\n```\n\n## Basic usage \n\nNautikos is configured through a YAML-file (`./nautikos.yaml`), that specifies where the manifests for the different images and environments can be found: \n\n```yaml\nenvironments: \n# An environment is basically a collection of manifests that you want to \n# update simultaneously. \n- name: prod \n  manifests: \n  - path: path/to/prod-env-1-file.yaml  # Path relative to configuration file\n    type: kubernetes  # Type can be 'kubernetes', 'kustomize' or 'helm'\n  - path: path/to/prod-env-2-file.yaml \n    type: kustomize\n    repositories:  # Optional specification of repositories to be modified for more granular control\n      - repository-b\n      - repository-c\n- name: dev\n  manifests: \n  - path: path/to/dev-env-file.yaml\n    type: helm\n```\n\nNext, you can run Nautikos to update the image tags of specific images in different environments.\n\n```bash\nnautikos --env prod repository-a 1.2.3  # Updates all occurences of the image `repository-a` to `1.2.3` in `prod-env-1-file.yaml`\nnautikos --env prod repository-b 1.2.3  # Updates all occurences of the image `repository-b` to `1.2.3` in `prod-env-1-file.yaml` and `prod-env-1-file.yaml`\nnautikos --env dev repository-c dev-1.2.3  # Updates all occurences of the image `repository-c` to `dev-1.2.3` in `dev-env-file.yaml`\n```\n\n## Supported tools\n\nThe tool works with standard **Kubernetes** manifests, **Kustomize**, and **Helm**. Each have their own format for defining image tags. \n\n```yaml\n# Kubernetes manifests\nspec:\n  template:\n    spec:\n      containers:\n      - image: some-repository:tag\n\n# Kustomize\nimages: \n- name: some-repository\n  newTag: tag \n\n# Helm \nimage: \n- repository: some-repository \n  tag: tag \n```\n\n## Advanced usage\n\nNautikos takes several options: \n\n* `--dry-run`: prints the lines that would be modified, but doesn't edit in place \n* `--config config-file.yaml`: path to config YAML, default is `./nautikos.yaml`\n\n## Alternatives \n\nThere are basically three alternatives to do the same thing: \n\n* **Update manifests manually** - of course this works, but this is not really proper CD\n* **Write your own bash scripts in a pipeline using a tool like `sed`** - This works, but having to write this logic for every project is tedious. \n* **Use a tool like [Argo-CD Image updater](https://argocd-image-updater.readthedocs.io/en/stable/)** - very nice, but a bit heavy-weight, not very actively developed, and doesn't seem to support Azure Container Registry. \n\n## Notes \n\nMultiple YAML docs in one file is not yet supported. \n\n## Dependencies \n\n* **`typer`** - for creating a CLI \n* **`ruamel.yaml`** - for handling YAML files while maintaining ordering and comments\n",
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
