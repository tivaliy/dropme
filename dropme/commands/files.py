#
#    Copyright 2017 Vitalii Kulanov
#

import abc
import argparse
import datetime
import os

from dropbox import exceptions
from dropbox import files

from . import base
from .. import error
from ..common import utils


class FileUpload(base.BaseCommand):
    """
    Uploads a file to a specified directory.

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
    def _build_destination_path(src_path, dst_path=None):
        if dst_path is None:
            return os.path.join('/', os.path.basename(src_path))
        return utils.normalize_path(dst_path)

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
            help='The path to the file to upload.'
        )
        parser.add_argument(
            'path',
            nargs='?',
            help='The path of the directory to upload file,'
                 'defaults to the root.'
        )
        parser.add_argument(
            '-r', '--auto-rename',
            action='store_true',
            help='Whether the file should be renamed '
                 'if there is a name conflict.'
        )
        return parser

    def take_action(self, parsed_args):
        dst_path = self._build_destination_path(parsed_args.file,
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


class FileFolderDelete(base.BaseCommand, base.FileFolderMixIn):
    """
    Deletes a file or a folder at a given path.

    If the path is a folder, all its content will be deleted too.
    """

    def get_parser(self, prog_name):
        parser = super(FileFolderDelete, self).get_parser(prog_name)
        parser.add_argument(
            'path',
            help='The path of the file or folder to delete.'
        )
        return parser

    def take_action(self, parsed_args):
        path = utils.normalize_path(parsed_args.path)
        try:
            response = self.client.files_delete_v2(path)
        except exceptions.ApiError as exc:
            msg = "An error occurred while deleting '{0}': {1}.".format(
                parsed_args.path, exc.error)
            raise error.ActionException(msg) from exc
        msg = "{0} '{1}' {2}was successfully deleted from '{3}'.\n".format(
            self.get_entity_type(response.metadata).capitalize(),
            response.metadata.name,
            '' if self.is_file(response.metadata) else 'and all its content ',
            response.metadata.path_display)
        self.stdout.write(msg)


class FileDownload(base.BaseCommand):
    """
    Downloads a file at a given local path.
    """

    def get_parser(self, prog_name):
        parser = super(FileDownload, self).get_parser(prog_name)
        parser.add_argument(
            'path',
            metavar='DROPBOX_FILE',
            help='The path of the file to download.'
        )
        parser.add_argument(
            'file',
            metavar='LOCAL_FILE',
            nargs='?',
            help='The path of the file to save data, '
                 'defaults to current working directory.'
        )
        parser.add_argument(
            '--revision',
            help='The revision of a file.'
        )
        return parser

    def take_action(self, parsed_args):
        path = utils.normalize_path(parsed_args.path)
        if not parsed_args.file:
            dst_path = os.path.join(os.getcwd(), os.path.basename(path))
        else:
            dst_path = parsed_args.file

        try:
            response = self.client.files_download_to_file(
                dst_path, path, rev=parsed_args.revision)
        except (exceptions.ApiError, IOError, OSError) as exc:
            msg = ("An error occurred while downloading '{0}' file as '{1}': "
                   "{2}.".format(path, dst_path,
                                 exc.error if hasattr(exc, 'error') else exc))
            raise error.ActionException(msg) from exc
        msg = ("File '{0}' (rev={1}, size {2}) from '{3}' was successfully "
               "downloaded as '{4}'.\n".format(
                response.name, response.rev, utils.convert_size(response.size),
                response.path_display, dst_path))
        self.stdout.write(msg)


class FileFolderStatusShow(base.BaseShowCommand, base.FileFolderMixIn):
    """
    Shows status for a specified file or folder.
    """
    columns = ('name', 'type', 'path')

    def get_parser(self, prog_name):
        parser = super(FileFolderStatusShow, self).get_parser(prog_name)
        parser.add_argument(
            'path',
            help='The path to the file to get metadata.'
        )
        parser.add_argument(
            '-i', '--include-media-info',
            action='store_true',
            help='Show media info for file with photo or video content.'
        )
        parser.add_argument(
            '-d', '--include-deleted',
            action='store_true',
            help='Fetch data for deleted file sor folder.'
        )
        parser.add_argument(
            '-m', '--include-has-members',
            action='store_true',
            help='Indicate whether or not file has any explicit shared members'
        )
        return parser

    def take_action(self, parsed_args):
        path = utils.normalize_path(parsed_args.path)
        has_members = parsed_args.include_has_members
        try:
            response = self.client.files_get_metadata(
                path,
                include_media_info=parsed_args.include_media_info,
                include_deleted=parsed_args.include_deleted,
                include_has_explicit_shared_members=has_members
            )
        except (exceptions.ApiError, exceptions.BadInputError) as exc:
            msg = "status: cannot fetch metadata for '{0}': {1}.".format(
                path, exc.error if hasattr(exc, 'error') else exc.message)
            raise error.ActionException(msg) from exc
        data = {'name': response.name,
                'path': response.path_display}
        # TODO vkulanov Add more output results
        if self.is_file(response):
            self.columns += ('size', 'client_modified', 'server_modified',
                             'revision', 'parent_shared_folder_id',
                             'has_explicit_shared_members', 'content_hash')
            data.update(
                {'type': 'file',
                 'size': utils.convert_size(response.size),
                 'client_modified': response.client_modified.isoformat(' '),
                 'server_modified': response.server_modified.isoformat(' '),
                 'revision': response.rev,
                 'parent_shared_folder_id': response.parent_shared_folder_id,
                 'content_hash': response.content_hash,
                 'has_explicit_shared_members':
                     response.has_explicit_shared_members})
            if response.media_info and parsed_args.include_media_info:
                metadata = response.media_info.get_metadata()
                self.columns += ('width', 'height', 'time_taken')
                data.update({'width': metadata.dimensions.width,
                             'height': metadata.dimensions.height,
                             'time_taken': metadata.time_taken.isoformat(' ')})
                if isinstance(metadata, files.VideoMetadata):
                    self.columns += ('duration',)
                    data['duration'] = datetime.timedelta(
                        milliseconds=metadata.duration)
        else:
            self.columns += ('shared_folder_id', 'parent_shared_folder_id',
                             'property_groups')
            data.update(
                {'type': 'directory',
                 'shared_folder_id': response.shared_folder_id,
                 'parent_shared_folder_id': response.parent_shared_folder_id,
                 'property_groups': response.property_groups})
        data = utils.get_display_data_single(self.columns, data)
        return self.columns, data


class BaseFileFolderAction(base.BaseCommand, base.FileFolderMixIn):
    """
    Base class to perform move or copy action on files/folders.
    """

    @property
    @abc.abstractmethod
    def action_type(self):
        """Type of action: 'copy'|'move'

        :rtype: str
        """

    def get_parser(self, prog_name):
        parser = super(BaseFileFolderAction, self).get_parser(prog_name)
        parser.add_argument(
            'from_path',
            help="Path to a file or folder in the user's Dropbox "
                 "to {0}.".format(self.action_type)
        )
        parser.add_argument(
            'to_path',
            help="Destination path in the users's Dropbox. Will be created"
                 "if does not exist."
        )
        parser.add_argument(
            '--allow-shared-folder',
            action='store_true',
            help='Whether or not allow to {0} '
                 'to a shared folder.'.format(self.action_type)
        )
        parser.add_argument(
            '-r', '--auto-rename',
            action='store_true',
            help='Whether the file should be renamed '
                 'if there is a name conflict.'
        )
        parser.add_argument(
            '--allow-ownership-transfer',
            action='store_true',
            help='Allow moves by owner even if it would result in an '
                 'ownership transfer for the content being moved. '
                 'This does not apply to copies.'
        )
        return parser

    def take_action(self, parsed_args):
        actions = {'copy': self.client.files_copy_v2,
                   'move': self.client.files_move_v2}
        aliases = {'copy': ('cp', 'copied'), 'move': ('mv', 'moved')}
        from_path = utils.normalize_path(parsed_args.from_path)
        to_path = utils.normalize_path(parsed_args.to_path)
        try:
            response = actions[self.action_type](
                from_path, to_path, autorename=parsed_args.auto_rename,
                allow_shared_folder=parsed_args.allow_shared_folder,
                allow_ownership_transfer=parsed_args.allow_ownership_transfer
            )
        except exceptions.ApiError as exc:
            msg = "{0}: cannot {1} from '{2}' to '{3}': {4}.".format(
                aliases[self.action_type][0], self.action_type, from_path,
                to_path,  exc.error)
            raise error.ActionException(msg) from exc
        msg = ("{0} '{1}' {2}was successfully {3} from '{4}' as '{5}'.\n"
               "".format(self.get_entity_type(response.metadata).capitalize(),
                         os.path.basename(from_path),
                         'and all its content ' if self.is_folder(
                             response.metadata) else '',
                         aliases[self.action_type][1],
                         from_path, response.metadata.path_display))
        self.stdout.write(msg)


class FileFolderCopy(BaseFileFolderAction):
    """
    Copies a file or folder to a different location in the user’s Dropbox.

    If the source path is a folder all its content will be copied.
    If destination path doesn't exist it will be created.
    """

    action_type = 'copy'


class FileFolderMove(BaseFileFolderAction):
    """
    Moves a file or folder to a different location in the user’s Dropbox.

    If the source path is a folder all its content will be moved.
    If destination path doesn't exist it will be created.
    """

    action_type = 'move'
