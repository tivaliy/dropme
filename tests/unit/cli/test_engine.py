#
#    Copyright 2017 Vitalii Kulanov
#

import shlex

import pytest


from dropme.app import main as main_mod


class BaseCLITest(object):
    """
    Base class for testing the new CLI.
    """

    @pytest.fixture
    def mock_dropbox(self, mocker):
        m_client = mocker.patch('dropme.client.dropbox.Dropbox')
        return m_client

    @pytest.fixture
    def mock_client(self, mock_dropbox):
        return mock_dropbox.return_value

    @staticmethod
    def exec_command(command=''):
        """
        Executes dropme with the specified arguments.
        """
        argv = shlex.split(command)
        if '--debug' not in argv:
            argv = ['--debug'] + argv

        return main_mod(argv=argv)
