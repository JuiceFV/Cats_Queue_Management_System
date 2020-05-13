"""In this file you can find the configuration-processing function.
"""


from pathlib import Path
import yaml


# Gives the permit for the import only for the 'load_config'
__all__ = ('load_config',)


def load_config(cfg_file=None, test=None, debug=None, release=None):
    """This function handle and upload/setup the configuration into the application.

    Keyword arguments:
    cfg_file -- file which handling.
    test -- the sign if test mode (run-type) is on
    debug -- the sign if debug mode (run-type) is on
    release -- the sign if release mode (run-type) is on

    Returns unpacked config.

    """

    # if the file wasn't passed as argument it's looks for the default file.
    default_file = Path(__file__).parent.parent / 'config.yaml'
    with open(default_file, 'r') as f:
        config = yaml.safe_load(f)

    cfg_dict = {}
    # if configuration file exists then upload the config as dict.
    if cfg_file:
        cfg_dict = yaml.safe_load(cfg_file)

    # if dict doesn't empty then update the config.
    if cfg_dict:
        config.update(**cfg_dict)

    # There are 3 possible run-type options
    # If they were passed as an argument therefore we setting them up.
    if test:
        config['run_type'] = 'test'
    elif debug:
        config['run_type'] = 'debug'
    elif release:
        config['run_type'] = 'release'

    return config
