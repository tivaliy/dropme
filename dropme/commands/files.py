#
#    Copyright 2017 Vitalii Kulanov
#

import argparse
import os

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
            'path',
            nargs='?',
            help='path to the directory for printing its contents,'
                 'defaults to the root'
        )
        parser.add_argument(
            '-l', '--long-listing',
            action='store_true',
            help='use a long listing format'
        )
        return parser

    def take_action(self, parsed_args):
        path = '/' + parsed_args.path if parsed_args.path else ''
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


class FileUpload(base.BaseCommand):
    """
    Uploads file to a specified directory.

    If destination directory path doesn't exist it will be created
    """

    # Upload 32 MB of file contents per request
    CHUNK_SIZE = 32 * 1024 * 1024

    @staticmethod
    def _get_file_path(file_path):
        if not os.path.lexists(file_path):
            raise argparse.ArgumentTypeError(
                "File '{0}' does not exist".format(file_path))
        return file_path

    def upload_file(self, file_src, file_dst, autorename=False):
        file_size = os.path.getsize(file_src)
        response = None
        try:
            with open(file_src, 'rb') as f:
                if file_size <= self.CHUNK_SIZE:
                    response = self.client.files_upload(f.read(), file_dst,
                                                        autorename=autorename)
                else:
                    session_start = self.client.files_upload_session_start(
                        f.read(self.CHUNK_SIZE))
                    cursor = files.UploadSessionCursor(
                        session_id=session_start.session_id, offset=f.tell())
                    commit = files.CommitInfo(path=file_dst,
                                              autorename=autorename)
                    while f.tell() < file_size:
                        if file_size - f.tell() <= self.CHUNK_SIZE:
                            response = self.client.files_upload_session_finish(
                                f.read(self.CHUNK_SIZE), cursor, commit)
                        else:
                            self.client.files_upload_session_append_v2(
                                f.read(self.CHUNK_SIZE), cursor)
                            cursor.offset = f.tell()
        except exceptions.ApiError as exc:
            msg = "An error occurred while uploading '{0}': {1}.".format(
                file_src, exc.error.get_path().reason)
            raise error.ActionException(msg) from exc
        return response

    def get_parser(self, prog_name):
        parser = super(FileUpload, self).get_parser(prog_name)
        parser.add_argument(
            'file',
            type=self._get_file_path,
            help='file to upload'
        )
        parser.add_argument(
            'path',
            nargs='?',
            help='path to the directory to upload file,'
                 'defaults to the root'
        )
        parser.add_argument(
            '-r', '--auto-rename',
            action='store_true',
            help='whether the file should be renamed '
                 'if there is a name conflict'
        )
        return parser

    def take_action(self, parsed_args):
        path = '/{0}'.format(parsed_args.path
                             if parsed_args.path else parsed_args.file)
        self.stdout.write("Uploading '{0}' file to Dropbox as '{1}'"
                          "\n".format(parsed_args.file, path))
        response = self.upload_file(parsed_args.file, path)
        msg = ("File '{0}' ({1}) was successfully uploaded to Dropbox "
               "as '{2}'\n".format(parsed_args.file,
                                   utils.convert_size(response.size),
                                   response.path_display))
        self.stdout.write(msg)
