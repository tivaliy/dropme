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
    Tests for dropme files related commands.
    """

    @pytest.mark.parametrize('dst_path, autorename', [
        ('', False),
        ('/some/fake/path/fake_small_file.bin', True)
    ])
    def test_file_upload_at_once(self, mock_client, mocker, tmpdir, dst_path,
                                 autorename):
        file_content = b'Some fake data to be send'
        mocker.patch('dropme.commands.files.FileUpload.CHUNK_SIZE',
                     new_callable=mocker.PropertyMock, return_value=1024)
        fake_file = tmpdir.join('fake_small_file.bin')
        fake_file.write(file_content)
        file_size = os.path.getsize(fake_file.strpath)

        mock_client.files_upload.return_value = files.FileMetadata(
            path_display=dst_path if dst_path else '/' + fake_file.basename,
            size=file_size)

        args = 'upload {0} {1} {2}'.format(
            fake_file.strpath, dst_path, '--auto-rename' if autorename else '')
        self.exec_command(args)

        mock_client.files_upload.assert_called_once_with(
            file_content,
            dst_path if dst_path else '/' + fake_file.basename,
            autorename=autorename)

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

    @pytest.mark.parametrize('path, response', [
        ('fake_folder', files.DeleteResult(
            metadata=files.FolderMetadata(path_display='/fake_folder'))),
        ('/foo/folder', files.DeleteResult(
            metadata=files.FolderMetadata(path_display='/foo/bar/folder'))),
        ('/bar/some.log', files.DeleteResult(
            metadata=files.FileMetadata(path_display='/bar/some.log')))
    ])
    def test_delete_file_or_folder(self, mock_client, path, response):
        args = 'rm {0}'.format(path)
        path = path if path.startswith('/') else os.path.join('/', path)
        mock_client.files_delete_v2.return_value = response
        self.exec_command(args)
        mock_client.files_delete_v2.assert_called_once_with(path)

    def test_delete_w_non_specified_path_fail(self, mocker, capsys):
        mocker.patch('dropme.client.get_client')
        args = 'rm'
        with pytest.raises(SystemExit):
            self.exec_command(args)
        out, err = capsys.readouterr()
        assert "error: the following arguments are required: path" in err

    def test_delete_non_existing_folder_fail(self, mock_client):
        path = '/non/existing/path'
        mock_client.files_delete_v2.side_effect = exceptions.ApiError(
            request_id='ed9755c09d6f856ba81491ef2ec4a230',
            error=files.DeleteError('path_lookup',
                                    files.LookupError('not_found', None)),
            user_message_locale='',
            user_message_text=''
        )
        args = 'rm {0}'.format(path)
        with pytest.raises(error.ActionException) as excinfo:
            self.exec_command(args)
        mock_client.files_delete_v2.assert_called_once_with(path)
        assert "An error occurred while deleting '{0}':".format(
            path) in str(excinfo.value)

    @pytest.mark.parametrize('path, dst_path, rev, response', [
        ('root.folder.file', '', 'd5e0155e3', files.FileMetadata(
            name='root.folder.file', path_display='/root.folder.file',
            rev='d5e0155e3', size=1024 * 1024)),
        ('/empty/destination.file', '', 'a52715ee9', files.FileMetadata(
            name='destination.file', path_display='/empty/destination.file',
            rev='d5e0155e3', size=10)),
        ('/foo/bar.file', 'local/path.file', 'e320133f1', files.FileMetadata(
            name='bar.file', path_display='/foo/bar.file',
            rev='e320133f1', size=34524)),
        ('bar/some.log', 'bar/new_name.log', None, files.FileMetadata(
            name='some.log', path_display='/bar/some.log',
            rev='44eaa1002', size=563233467))
    ])
    def test_download_file(self, mocker, mock_client, path, dst_path, rev,
                           response):
        cwd = '/foo/bar'
        mocker.patch('dropme.commands.files.os.getcwd', return_value=cwd)
        args = 'download {0} {1} {2}'.format(
            path, dst_path, '--revision {0}'.format(rev) if rev else '')
        path = path if path.startswith('/') else os.path.join('/', path)
        dst_path = dst_path if dst_path else os.path.join(
            cwd, os.path.basename(path))
        mock_client.files_download_to_file.return_value = response
        self.exec_command(args)
        mock_client.files_download_to_file.assert_called_once_with(
            dst_path, path, rev=rev)

    def test_download_w_non_specified_path_fail(self, mocker, capsys):
        mocker.patch('dropme.client.get_client')
        args = 'download'
        with pytest.raises(SystemExit):
            self.exec_command(args)
        out, err = capsys.readouterr()
        msg = "error: the following arguments are required: DROPBOX_FILE"
        assert msg in err

    def test_download_non_existing_file_fail(self, mock_client):
        path = '/non/existing/path/fake.log'
        dst_path = '/my/local/path/fake.log'
        mock_client.files_download_to_file.side_effect = exceptions.ApiError(
            request_id='ed9755c09d6f856ba81491ef2ec4a230',
            error=files.DownloadError(
                'path', files.LookupError('not_found', None)),
            user_message_locale='',
            user_message_text=''
        )
        args = 'download {0} {1}'.format(path, dst_path)
        with pytest.raises(error.ActionException) as excinfo:
            self.exec_command(args)
        mock_client.files_download_to_file.assert_called_once_with(dst_path,
                                                                   path,
                                                                   rev=None)
        assert "An error occurred while downloading '{0}'".format(
            path) in str(excinfo.value)

    @pytest.mark.parametrize(
        'path, include_media_info, include_deleted, include_has_members, '
        'response',
        [('/root.folder.file', False, False, False, files.FileMetadata(
            name='root.folder.file', path_display='/root.folder.file',
            rev='d5e0155e3', size=1024, content_hash='20978837' * 8,
            client_modified=datetime(2017, 10, 29, 11, 12, 54),
            server_modified=datetime(2017, 10, 29, 11, 12, 54))),
         ('/dummy/video.avi', True, False, False, files.FileMetadata(
             name='video.avi', path_display='/dummy/video.avi',
             rev='d5e0155e3', size=143234451, content_hash='da364337' * 8,
             client_modified=datetime(2017, 10, 29, 11, 12, 54),
             server_modified=datetime(2017, 10, 29, 11, 12, 54),
             media_info=files.MediaInfo('metadata', files.VideoMetadata(
                 files.Dimensions(768, 1024), duration=3123451,
                 time_taken=datetime(2016, 10, 17, 10, 10, 54))))),
         ('/foo/bar/folder', True, True, True, files.FolderMetadata(
            name='folder', path_display='/foo/bar/folder'))])
    def test_show_status_for_file_or_folder(
            self, mock_client, path, include_media_info, include_deleted,
            include_has_members, response):
        mock_client.files_get_metadata.return_value = response
        args = 'status {0} {1} {2} {3}'.format(
            path,
            '--include-media-info' if include_media_info else '',
            '--include-deleted' if include_deleted else '',
            '--include-has-members' if include_has_members else '')
        self.exec_command(args)
        mock_client.files_get_metadata.assert_called_once_with(
            path,
            include_media_info=include_media_info,
            include_deleted=include_deleted,
            include_has_explicit_shared_members=include_has_members)

    def test_show_status_w_non_specified_path_fail(self, mocker, capsys):
        mocker.patch('dropme.client.get_client')
        args = 'status'
        with pytest.raises(SystemExit):
            self.exec_command(args)
        out, err = capsys.readouterr()
        assert "error: the following arguments are required: path"in err

    def test_show_status_non_existing_file_fail(self, mock_client):
        path = '/non/existing/path/fake.log'
        mock_client.files_get_metadata.side_effect = exceptions.ApiError(
            request_id='ed9755c09d6f856ba81491ef2ec4a230',
            error=files.GetMetadataError(
                'path', files.LookupError('not_found', None)),
            user_message_locale='',
            user_message_text=''
        )
        args = 'status {0}'.format(path)
        with pytest.raises(error.ActionException) as excinfo:
            self.exec_command(args)
        mock_client.files_get_metadata.assert_called_once_with(
            path, include_media_info=False, include_deleted=False,
            include_has_explicit_shared_members=False)
        assert "status: cannot fetch metadata for '{0}'".format(path) in str(
            excinfo.value)
