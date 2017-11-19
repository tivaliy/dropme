#
#    Copyright 2017 Vitalii Kulanov
#

from dropbox import exceptions
from dropbox import files

from . import base
from .. import error
from ..common import utils


def is_file(entity):
    return isinstance(entity, files.FileMetadata)


class FolderList(base.BaseListCommand):
    """
    List directory content.
    """

    columns = ('name',)

    @staticmethod
    def _get_entry_name_by_type(entry):
        return entry.name if is_file(entry) else entry.name + '/'

    def get_parser(self, prog_name):
        parser = super(FolderList, self).get_parser(prog_name)
        parser.add_argument(
            'source',
            nargs='?',
            help='path to the directory for printing its contents'
        )
        parser.add_argument(
            '-l',
            '--long-listing',
            action='store_true',
            help='use a long listing format'
        )
        return parser

    def take_action(self, parsed_args):
        source = '/' + parsed_args.source if parsed_args.source else ''
        try:
            response = self.client.files_list_folder(source)
        except exceptions.ApiError as exc:
            msg = "ls: cannot access '{0}': No such directory".format(source)
            raise error.ActionException(msg) from exc
        if parsed_args.long_listing:
            self.columns = ('type', 'size', 'last_modified', 'name')
            data = [
                {'name': self._get_entry_name_by_type(entry),
                 'type': '-' if is_file(entry) else 'd',
                 'size': utils.convert_size(entry.size)
                         if is_file(entry) else '',
                 'last_modified': entry.server_modified.isoformat(' ')
                         if is_file(entry) else ''
                 } for entry in response.entries]
        else:
            data = [{'name': self._get_entry_name_by_type(entry)}
                    for entry in response.entries]
        data = utils.get_display_data_multi(self.columns, data,
                                            sort_by=parsed_args.sort_columns)
        return self.columns, data
