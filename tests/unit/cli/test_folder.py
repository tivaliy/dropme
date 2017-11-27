#
#    Copyright 2017 Vitalii Kulanov
#

from datetime import datetime

import pytest
from dropbox import files
from dropbox import exceptions

from .test_engine import BaseCLITest
from dropme import error


class TestFolderCommand(BaseCLITest):
    """
    Tests for dropme folders related commands.
    """

    def test_files_and_folders_list_root(self, mock_client):
        args = 'ls'
        mock_client.files_list_folder.return_value = files.ListFolderResult(
            entries=[files.FolderMetadata(name='fake-folder-1'),
                     files.FileMetadata(name='fake-file-1')])
        self.exec_command(args)
        mock_client.files_list_folder.assert_called_once_with('')

    def test_files_and_folders_list_w_path(self, mock_client):
        path = 'fake_folder_path'
        args = 'ls {0} --long-listing'.format(path)
        mock_client.files_list_folder.return_value = files.ListFolderResult(
            entries=[files.FolderMetadata(name='fake-folder-1'),
                     files.FileMetadata(name='fake-file-1', size=1234,
                                        server_modified=datetime(2017, 10, 29,
                                                                 11, 12, 54))])
        self.exec_command(args)
        mock_client.files_list_folder.assert_called_once_with('/' + path)

    def test_files_and_folders_list_non_existing_path_fail(self, mock_client):
        path = 'non_existing_folder_path'
        args = 'ls {0}'.format(path)
        mock_client.files_list_folder.side_effect = exceptions.ApiError(
            request_id='ed9755c09d6f856ba81491ef2ec4a230',
            error=files.ListFolderError(
                'path', files.LookupError('not_found', None)),
            user_message_locale='',
            user_message_text=''
        )
        with pytest.raises(error.ActionException) as excinfo:
            self.exec_command(args)
        mock_client.files_list_folder.assert_called_once_with('/' + path)
        assert "ls: cannot access '/{0}'".format(path) in str(excinfo.value)
