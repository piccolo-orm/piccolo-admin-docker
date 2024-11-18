import typing as t

import yaml
from models import AdditionalConfig


def load_yaml() -> dict[str, t.Any]:
    with open("config.yaml") as stream:
        try:
            admin_config = yaml.safe_load(stream)
            return AdditionalConfig(**admin_config)
        except yaml.YAMLError as exc:
            raise exc


additional_config = load_yaml()
