#
#    Copyright 2017 Vitalii Kulanov
#

import os

from datetime import datetime

import pytest
from dropbox import files
from dropbox import exceptions

from .test_engine import BaseCLITest
from dropme import error


class TestFilesCommand(BaseCLITest):
    """
    Tests for dropme files/folders manipulation related commands.
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

    @pytest.mark.parametrize('dst_path', [
        '',
        '/some/fake/path/fake_small_file.bin'
    ])
    def test_file_upload_at_once(self, mock_client, mocker, tmpdir, dst_path):
        file_content = b'Some fake data to be send'
        mocker.patch('dropme.commands.files.FileUpload.CHUNK_SIZE',
                     new_callable=mocker.PropertyMock, return_value=1024)
        fake_file = tmpdir.join('fake_small_file.bin')
        fake_file.write(file_content)
        file_size = os.path.getsize(fake_file.strpath)

        mock_client.files_upload.return_value = files.FileMetadata(
            path_display=dst_path if dst_path else '/' + fake_file.basename,
            size=file_size)

        args = 'upload {0} {1}'.format(fake_file.strpath, dst_path)
        self.exec_command(args)

        mock_client.files_upload.assert_called_once_with(
            file_content,
            dst_path if dst_path else '/' + fake_file.basename,
            autorename=False)

    def test_file_upload_in_parts_to_root(self, mock_client, mocker, tmpdir):
        chunk_size = 10
        file_content = b'Some fake data to be uploaded by chunks'
        mocker.patch('dropme.commands.files.FileUpload.CHUNK_SIZE',
                     new_callable=mocker.PropertyMock, return_value=chunk_size)
        fake_file = tmpdir.join('fake_large_file.bin')
        fake_file.write(file_content)
        file_size = os.path.getsize(fake_file.strpath)
        # Count the last chunk size that expected to be passed
        chunk = file_size % chunk_size
        trailing_chunk_size = chunk_size if chunk == 0 else chunk

        m_session_start = mock_client.files_upload_session_start.return_value
        m_session_start.session_id = '4jFsLN63sa840dsw3'
        fake_resp = files.FileMetadata(path_display='/' + fake_file.basename,
                                       size=file_size)
        mock_client.files_upload_session_finish.return_value = fake_resp

        args = 'upload {0}'.format(fake_file.strpath)
        self.exec_command(args)

        mock_client.files_upload_session_start.assert_called_once_with(
            file_content.decode('utf-8')[:chunk_size].encode())
        mock_client.files_upload_session_finish.assert_called_once_with(
            file_content.decode('utf-8')[-trailing_chunk_size:].encode(),
            mocker.ANY, mocker.ANY)
        mock_client.assert_has_calls(
            [mocker.call.files_upload_session_append_v2(mocker.ANY,
                                                        mocker.ANY)],
            any_order=True)

    def test_upload_non_existing_file_fail(self, mocker, capsys):
        mocker.patch('dropme.client.get_client')
        mocker.patch('dropme.commands.files.os.path.lexists',
                     return_value=False)
        fake_file = '/non/existing/file.path'
        args = 'upload {0}'.format(fake_file)
        with pytest.raises(SystemExit):
            self.exec_command(args)
        out, err = capsys.readouterr()
        assert "File '{0}' does not exist".format(fake_file) in err

    def test_upload_file_insufficient_space_fail(self, mock_client, tmpdir):
        fake_file = tmpdir.join('fake_small_file.bin')
        fake_file.write('')
        args = 'upload {0}'.format(fake_file)
        mock_client.files_upload.side_effect = exceptions.ApiError(
            request_id='ed9755c09d6f856ba81491ef2ec4a230',
            error=files.UploadError(
                'path', files.UploadWriteFailed(
                    reason=files.WriteError('insufficient_space', None),
                    upload_session_id='')),
            user_message_locale='',
            user_message_text=''
        )
        with pytest.raises(error.ActionException) as excinfo:
            self.exec_command(args)
        assert "An error occurred while uploading '{}'".format(
            fake_file) in str(excinfo.value)
