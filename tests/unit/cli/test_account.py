#
#    Copyright 2017 Vitalii Kulanov
#

from dropbox import users

from .test_engine import BaseCLITest


class TestAccountCommand(BaseCLITest):
    """
    Tests for dropme account related commands.
    """

    def test_account_info_show(self, mock_client):
        args = 'whoami'
        mock_client.users_get_current_account.return_value = users.FullAccount(
            name=users.Name(display_name='John Doe'),
            email='j.doe.example.com',
            country='UA')
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
