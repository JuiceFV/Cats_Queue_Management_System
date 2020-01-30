from pathlib import Path
import yaml

__all__ = ('load_config',)


def load_config(cfg_file=None):
    default_file = Path(__file__).parent / 'config.yaml'
    with open(default_file, 'r') as f:
        config = yaml.safe_load(f)

    cfg_dict = {}
    if cfg_file:
        cfg_dict = yaml.safe_load(cfg_file)

    if cfg_dict:
        config.update(**cfg_dict)

    return config
