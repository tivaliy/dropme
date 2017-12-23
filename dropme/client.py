#
#    Copyright 2017 Vitalii Kulanov
#

import os

import dropbox

from . import error
from .common import utils


def get_client(token=None):
    token = (token or
             os.environ.get('DBX_AUTH_TOKEN') or
             get_settings().get('token'))
    if not token:
        raise ValueError("Token not found.")
    return dropbox.Dropbox(token)


def get_settings(file_path=None):
    """
    Get Dropme client configuration from 'settings.yaml' file.

    If path to configuration 'settings.yaml' not specified (None), then
    first try to get it from local directory and then from user .config one

    :param file_path: string that contains path to configuration file
    :raises: error.ConfigNotFoundException if configuration not specified
    """

    config_path = None

    user_config = os.path.join(os.path.expanduser('~'), '.config',
                               'dropme', 'settings.yaml')
    local_config = os.path.join(os.path.dirname(__file__), 'settings.yaml')

    if file_path is not None:
        config_path = file_path
    else:
        if os.path.isfile(local_config):
            config_path = local_config
        elif os.path.isfile(user_config):
            config_path = user_config

    if config_path is None:
        raise error.ConfigNotFoundException("Configuration 'settings.yaml' "
                                            "file not found.")

    try:
        config_data = utils.read_yaml_file(config_path)
    except (OSError, IOError):
        msg = "Could not read settings from {0}.".format(file_path)
        raise error.InvalidFileException(msg)
    return config_data
