"""In this file you can find the configuration-processing function.

Import packages:
pathlib.Path -- package for the ease path definition
yaml -- package for the yaml conversion from the config.yaml

Functions:
load_config(cfg_file) --

"""


from pathlib import Path
import yaml


# Gives the permit for the import only for the 'load_config'
__all__ = ('load_config',)


def load_config(cfg_file=None, test=None, debug=None, release=None):
    """This function handle and upload the configuration into the application.

    Keyword arguments:
    cfg_file -- file which handling.

    Looking for the default configuration file in the "application" - directory.
    Upload it into the config. Further it will be uploaded into the application.
    Returns unpacked config.

    """

    # if the file wasn't passed as argument it's looks for the default file.
    default_file = Path(__file__).parent / 'config.yaml'
    with open(default_file, 'r') as f:
        config = yaml.safe_load(f)

    cfg_dict = {}
    # if configuration file exists then upload the config as dict.
    if cfg_file:
        cfg_dict = yaml.safe_load(cfg_file)

    # if dict doesn't empty then updated the config.
    if cfg_dict:
        config.update(**cfg_dict)

    # There are 3 possible run-type options
    # If they were passed as an argument therefore we changing it
    if test:
        config['run_type'] = 'test'
    elif debug:
        config['run_type'] = 'debug'
    elif release:
        config['run_type'] = 'release'

    return config
