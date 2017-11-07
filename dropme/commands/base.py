#
#    Copyright 2017 Vitalii Kulanov
#

from cliff import command

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
