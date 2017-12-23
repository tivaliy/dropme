#
#    Copyright 2017 Vitalii Kulanov
#

import os

import pytest
import yaml

from dropme import client
from dropme import error


def test_get_client_w_token(mocker):
    token = '4145225aaFKL0dDlKY0323bcc8c37'
    m_dropbox = mocker.patch('dropme.client.dropbox.Dropbox')
    client.get_client(token=token)
    m_dropbox.assert_called_once_with(token)


def test_get_client_w_token_from_environment_variable(mocker, monkeypatch):
    token = '4145225aaFKL0dDlKY0323bcc8c37'
    monkeypatch.setitem(os.environ, 'DBX_AUTH_TOKEN', token)
    m_dropbox = mocker.patch('dropme.client.dropbox.Dropbox')
    client.get_client()
    m_dropbox.assert_called_once_with(token)


def test_get_client_wo_token_fail(mocker):
    m_get_settings = mocker.patch('dropme.client.get_settings')
    m_get_settings.return_value = {}
    with pytest.raises(ValueError) as excinfo:
        client.get_client(token=None)
    assert "Token not found." in str(excinfo.value)


def test_get_settings_from_non_existing_file_fail(mocker):
    m_path = mocker.patch('dropme.client.os.path')
    m_path.join.side_effect = ['/home/fake_user/.config/dropme/settings.yaml',
                               'some/fake/path/to/settings.yaml']
    m_path.isfile.side_effect = [False, False]
    with pytest.raises(error.ConfigNotFoundException) as excinfo:
        client.get_settings()
    assert "file not found." in str(excinfo.value)


@pytest.mark.parametrize('file_path, side_effect', [
    ('settings.yaml', [False, False]),  # file_path
    (None, [True, False]),              # local_path
    (None, [False, True]),              # user_path
])
def test_get_settings_from_file(mocker, file_path, side_effect):
    settings = {'token': 'F0ssXxcSj23fdFskFGsiDSJbJkHwk942'}
    m_path = mocker.patch('dropme.client.os.path')
    m_path.join.side_effect = ['/home/fake_user/.config/dropme/settings.yaml',
                               'some/fake/path/to/settings.yaml']
    m_path.isfile.side_effect = side_effect
    m_open = mocker.mock_open(read_data=yaml.safe_dump(settings))
    mocker.patch('dropme.common.utils.open', m_open)
    assert settings == client.get_settings(file_path=file_path)


def test_get_settings_from_bad_file_format_fail(mocker):
    m_path = mocker.patch('dropme.client.os.path')
    m_path.join.side_effect = ['/home/fake_user/.config/dropme/settings.yaml',
                               'some/fake/path/to/settings.yaml']
    m_path.isfile.side_effect = [True, False]
    m_open = mocker.mock_open()
    m_open.side_effect = IOError
    mocker.patch('dropme.common.utils.open', m_open)
    with pytest.raises(error.InvalidFileException) as excinfo:
        client.get_settings()
    assert "Could not read settings" in str(excinfo.value)
