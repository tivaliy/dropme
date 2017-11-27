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

    @pytest.mark.parametrize('path, autorename', [
        ('fake_folder', False),
        ('some/new/path', True),
        ('/foo/bar/path', False)
    ])
    def test_create_folder(self, mock_client, path, autorename):
        args = 'mkdir {0} {1}'.format(
            path, '--auto-rename' if autorename else '')
        path = path if path.startswith('/') else '/' + path
        response = files.CreateFolderResult(metadata=files.FolderMetadata(
            path_display=path))
        mock_client.files_create_folder_v2.return_value = response
        self.exec_command(args)
        mock_client.files_create_folder_v2.assert_called_once_with(
            path, autorename=autorename)

    def test_create_folder_malformed_path_fail(self, mock_client):
        path = '/malformed_path/'
        mock_client.files_create_folder_v2.side_effect = exceptions.ApiError(
            request_id='ed9755c09d6f856ba81491ef2ec4a230',
            error=files.CreateFolderError(
                'path', files.WriteError('malformed_path', None)),
            user_message_locale='',
            user_message_text=''
        )
        args = 'mkdir {0}'.format(path)
        with pytest.raises(error.ActionException) as excinfo:
            self.exec_command(args)
        mock_client.files_create_folder_v2.assert_called_once_with(
            path, autorename=False)
        assert "mkdir: cannot create directory '{0}'".format(
            path) in str(excinfo.value)

    def test_create_non_specified_folder_path_fail(self, mocker, capsys):
        empty_path_parameter = ''
        mocker.patch('dropme.client.get_client')
        args = 'mkdir {0}'.format(empty_path_parameter)
        with pytest.raises(SystemExit):
            self.exec_command(args)
        out, err = capsys.readouterr()
        assert "error: the following arguments are required: path" in err
