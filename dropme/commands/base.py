#
#    Copyright 2017 Vitalii Kulanov
#

import abc

from cliff import command
from cliff import lister
from cliff import show
from dropbox import files

from .. import client


class BaseCommand(command.Command):
    """Base Dropme Client command."""

    def __init__(self, *args, **kwargs):
        super(BaseCommand, self).__init__(*args, **kwargs)
        token = self.app.options.token if self.app else None
        self.client = client.get_client(token=token)

    @property
    def stdout(self):
        """Shortcut for self.app.stdout."""
        return self.app.stdout


class BaseShowCommand(show.ShowOne, BaseCommand):
    """Shows detailed information about the entity."""

    @property
    @abc.abstractmethod
    def columns(self):
        """Names of columns in the resulting table as a tuple."""


class BaseListCommand(lister.Lister, BaseCommand):
    """List all entities."""

    @property
    @abc.abstractmethod
    def columns(self):
        """Names of columns in the resulting table as a tuple."""


class FileFolderMixIn(object):
    """MixIn class for file and folder related actions."""

    @staticmethod
    def get_entity_type(metadata):
        """Returns the type of metadata object

        :param metadata: Metadata of the object
        :return: 'file'|'folder'|'deleted'
        """
        type_mapper = {'file': isinstance(metadata, files.FileMetadata),
                       'folder': isinstance(metadata, files.FolderMetadata),
                       'deleted': isinstance(metadata, files.DeletedMetadata)}
        return next(k for k, v in type_mapper.items() if v)

    @staticmethod
    def is_file(metadata):
        return isinstance(metadata, files.FileMetadata)

    @staticmethod
    def is_folder(metadata):
        return isinstance(metadata, files.FolderMetadata)
