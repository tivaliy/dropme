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


class FileUpload(base.BaseCommand):
    """
    Uploads file to a specified directory.

    If destination directory path doesn't exist it will be created.
    """

    # Upload 32 MB of file contents per request
    CHUNK_SIZE = 32 * 1024 * 1024

    @staticmethod
    def _get_file_path(file_path):
        if not os.path.lexists(file_path):
            raise argparse.ArgumentTypeError(
                "File '{0}' does not exist".format(file_path))
        return file_path

    @staticmethod
    def _normalize_destination_path(src_path, dst_path):
        if dst_path == '/':
            return os.path.join(dst_path, os.path.basename(src_path))
        return dst_path if dst_path.startswith('/') else os.path.join('/',
                                                                      dst_path)

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
            default='/',
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
        dst_path = self._normalize_destination_path(parsed_args.file,
                                                    parsed_args.path)
        self.stdout.write("Uploading '{0}' file to Dropbox as '{1}'"
                          "\n".format(parsed_args.file, dst_path))
        response = self.upload_file(parsed_args.file, dst_path,
                                    parsed_args.auto_rename)
        msg = ("File '{0}' ({1}) was successfully uploaded to Dropbox "
               "as '{2}'\n".format(parsed_args.file,
                                   utils.convert_size(response.size),
                                   response.path_display))
        self.stdout.write(msg)


class FileFolderDelete(base.BaseCommand):
    """
    Deletes the file or folder at a given path.

    If the path is a folder, all its contents will be deleted too.
    """

    def get_parser(self, prog_name):
        parser = super(FileFolderDelete, self).get_parser(prog_name)
        parser.add_argument(
            'path',
            help='path in the Dropbox environment to delete file or folder'
        )
        return parser

    def take_action(self, parsed_args):
        path = os.path.join('/', parsed_args.path) if parsed_args.path else ''
        try:
            response = self.client.files_delete_v2(path)
        except exceptions.ApiError as exc:
            print(exc.error)
            msg = "An error occurred while deleting '{0}': {1}.".format(
                parsed_args.path, exc.error)
            raise error.ActionException(msg) from exc
        msg = "{0} '{1}' was successfully deleted.\n".format(
            'File' if isinstance(response, files.FileMetadata) else 'Folder',
            response.metadata.path_display)
        self.stdout.write(msg)
