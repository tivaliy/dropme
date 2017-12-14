#
#    Copyright 2017 Vitalii Kulanov
#

import shlex

import pytest


from dropme.app import main as main_mod


class BaseCLITest(object):
    """
    Base class for testing CLI.
    """

    @pytest.fixture
    def mock_client(self, mocker):
        m_client = mocker.patch('dropme.client.get_client')
        return m_client.return_value

    @staticmethod
    def exec_command(command=''):
        """
        Executes dropme with the specified arguments.
        """
        argv = shlex.split(command)
        if '--debug' not in argv:
            argv = ['--debug'] + argv

        return main_mod(argv=argv)


class TestBaseCommand(BaseCLITest):
    """
    Tests for dropme base command.
    """

    def test_run_command_w_token_as_parameter(self, mocker):
        token = '4145225aaFKL0dDlKY0323bcc8c37'
        args = 'whoami --token {0}'.format(token)
        m_dropbox = mocker.patch('dropme.client.dropbox.Dropbox')
        self.exec_command(args)
        m_dropbox.assert_called_once_with(token)
