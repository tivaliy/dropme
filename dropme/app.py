#
#    Copyright 2017 Vitalii Kulanov
#

import logging
import sys

from cliff import app
from cliff.commandmanager import CommandManager


LOG = logging.getLogger(__name__)


class DropboxClient(app.App):
    """Main cliff application class.

    Initialization of the command manager and configuration of basic engines.
    """

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
    dropboxclient_app = DropboxClient(
        description='CLI tool for managing Dropbox environment.',
        version='0.0.1',
        command_manager=CommandManager('dropme', convert_underscores=True),
        deferred_help=True
    )
    return dropboxclient_app.run(argv)


def debug(name, cmd_class, argv=None):  # pragma: no cover
    """Helper for debugging single command without package installation."""
    import sys

    if argv is None:
        argv = sys.argv[1:]

    argv = [name] + argv + ["-v", "-v", "--debug"]
    cmd_mgr = CommandManager("test_dropme", convert_underscores=True)
    cmd_mgr.add_command(name, cmd_class)
    return DropboxClient(
        description="CLI tool for managing Dropbox environment.",
        version="0.0.1",
        command_manager=cmd_mgr
    ).run(argv)
