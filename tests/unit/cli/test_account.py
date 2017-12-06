#
#    Copyright 2017 Vitalii Kulanov
#

import pytest

from dropbox import users
from dropbox import users_common

from .test_engine import BaseCLITest


class TestAccountCommand(BaseCLITest):
    """
    Tests for dropme account related commands.
    """

    @pytest.mark.parametrize('arguments, response', [
        ('', users.FullAccount(
            name=users.Name(display_name='John Doe'),
            email='j.doe.example.com', country='UA',
            account_type=users_common.AccountType('basic', None))),
        ('--all', users.FullAccount(
            account_id='dbid:AAAw-03dfTrSkaZZlds34ass0212asTfvLn',
            name=users.Name(display_name='John Doe'),
            email='j.doe.example.com', country='UA',
            account_type=users_common.AccountType('business', None))),
    ])
    def test_account_info_show(self, mock_client, arguments, response):
        args = 'whoami {0}'.format(arguments)
        mock_client.users_get_current_account.return_value = response
        self.exec_command(args)
        mock_client.users_get_current_account.assert_called_once_with()

    def test_space_usage_show(self, mock_client):
        used = 100
        allocated = 100000
        mock_client.users_get_space_usage.return_value = users.SpaceUsage(
            used=used,
            allocation=users.SpaceAllocation(
                'individual', users.IndividualSpaceAllocation(allocated)))
        args = 'df'
        self.exec_command(args)
        mock_client.users_get_space_usage.assert_called_once_with()
