import yaml
from models import AdditionalConfig


def load_yaml() -> AdditionalConfig:
    with open("config.yaml") as file:
        admin_config = yaml.safe_load(file)
        return AdditionalConfig(**admin_config)


additional_config = load_yaml()
