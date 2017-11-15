#
#    Copyright 2017 Vitalii Kulanov
#

import abc

from cliff import command
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
