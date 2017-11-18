#
#    Copyright 2017 Vitalii Kulanov
#

import abc

from cliff import command
from cliff import lister
from cliff import show

from .. import client


class BaseCommand(command.Command):
    """Base Dropme Client command."""

    def __init__(self, *args, **kwargs):
        super(BaseCommand, self).__init__(*args, **kwargs)
        self.client = client.get_client()

    @property
    def stdout(self):
        """Shortcut for self.app.stdout."""
        return self.app.stdout


class BaseShowCommand(show.ShowOne, BaseCommand):
    """Shows detailed information about the entity."""

    @property
    @abc.abstractmethod
    def columns(self):
        """Names of columns in the resulting table."""


class BaseListCommand(lister.Lister, BaseCommand):
    """List all entities."""

    @property
    def default_sorting_by(self):
        """The first column in resulting table is default sorting field."""
        return [self.columns[0]]

    @property
    @abc.abstractmethod
    def columns(self):
        """Names of columns in the resulting table as a tuple."""

    def get_parser(self, prog_name):
        parser = super(BaseListCommand, self).get_parser(prog_name)

        # Add sorting key argument to the 'output formatters' group
        # (if exists), otherwise add it to the general group
        matching_groups = (group for group in parser._action_groups
                           if group.title == 'output formatters')

        group = next(matching_groups, None) or parser

        group.add_argument('-s',
                           '--sort-columns',
                           nargs='+',
                           metavar='SORT_COLUMN',
                           default=self.default_sorting_by,
                           help="Space separated list of keys for sorting the "
                                "data. Defaults to '{0}'. Wrong values are "
                                "ignored.".format(self.default_sorting_by))
        return parser
