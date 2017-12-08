#
#    Copyright 2017 Vitalii Kulanov
#

import os

from dropbox import exceptions

from . import base
from .. import error
from ..common import utils


class FolderList(base.BaseListCommand, base.FileFolderMixIn):
    """
    Lists directory content.
    """

    columns = ('name',)

    def _get_entry_name_by_type(self, entry):
        return entry.name if self.is_file(entry) else entry.name + '/'

    def get_parser(self, prog_name):
        parser = super(FolderList, self).get_parser(prog_name)
        parser.add_argument(
            'path',
            nargs='?',
            help='The path of the directory for printing its content,'
                 'defaults to the root.'
        )
        parser.add_argument(
            '-l', '--long-listing',
            action='store_true',
            help='Use a long listing format.'
        )
        return parser

    def take_action(self, parsed_args):
        path = os.path.join('/', parsed_args.path) if parsed_args.path else ''
        try:
            response = self.client.files_list_folder(path)
        except exceptions.ApiError as exc:
            msg = "ls: cannot access '{0}': {1}".format(
                path, exc.error.get_path())
            raise error.ActionException(msg) from exc
        if parsed_args.long_listing:
            self.columns = ('type', 'size', 'last_modified', 'name')
            data = [
                {'name': self._get_entry_name_by_type(entry),
                 'type': '-' if self.is_file(entry) else 'd',
                 'size': utils.convert_size(entry.size)
                         if self.is_file(entry) else '',
                 'last_modified': entry.server_modified.isoformat(' ')
                         if self.is_file(entry) else ''
                 } for entry in response.entries]
        else:
            data = [{'name': self._get_entry_name_by_type(entry)}
                    for entry in response.entries]
        data = utils.get_display_data_multi(self.columns, data,
                                            sort_by=parsed_args.sort_columns)
        return self.columns, data


class FolderCreate(base.BaseCommand):
    """
    Creates a folder at a given path.
    """

    def get_parser(self, prog_name):
        parser = super(FolderCreate, self).get_parser(prog_name)
        parser.add_argument(
            'path',
            help='The path of the folder to create.'
        )
        parser.add_argument(
            '-r', '--auto-rename',
            action='store_true',
            help='Whether the folder should be renamed '
                 'if there is a name conflict.'
        )
        return parser

    def take_action(self, parsed_args):
        path = utils.normalize_path(parsed_args.path)
        try:
            response = self.client.files_create_folder_v2(
                path, autorename=parsed_args.auto_rename)
        except exceptions.ApiError as exc:
            msg = "mkdir: cannot create directory '{0}': {1}".format(
                path, exc.error.get_path())
            raise error.ActionException(msg) from exc
        msg = "A new folder was successfully created at '{0}'.\n".format(
            response.metadata.path_display)
        self.stdout.write(msg)
