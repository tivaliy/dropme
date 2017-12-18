#
#    Copyright 2017 Vitalii Kulanov
#

import logging
import pkg_resources
import sys

from cliff import app
from cliff.commandmanager import CommandManager


LOG = logging.getLogger(__name__)


class DropboxClient(app.App):
    """Main cliff application class.

    Initialization of the command manager and configuration of basic engines.
    """

    def __init__(self):
        super(DropboxClient, self).__init__(
            description='CLI tool for managing Dropbox environment.',
            version=pkg_resources.require('dropme')[0].version,
            command_manager=CommandManager('dropme', convert_underscores=True),
            deferred_help=True
            )

    def build_option_parser(self, description, version, argparse_kwargs=None):
        option_parser = super(DropboxClient, self).build_option_parser(
            description, version, argparse_kwargs=argparse_kwargs)
        option_parser.add_argument(
            '-t', '--token',
            help='Dropbox token.'
        )
        return option_parser

    def run(self, argv):
        return super(DropboxClient, self).run(argv)

    def configure_logging(self):
        super(DropboxClient, self).configure_logging()
        root_logger = logging.getLogger('')
        root_logger.setLevel(logging.WARNING)


def main(argv=sys.argv[1:]):
    dropboxclient_app = DropboxClient()
    return dropboxclient_app.run(argv)
