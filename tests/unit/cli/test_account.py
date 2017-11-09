#
#    Copyright 2017 Vitalii Kulanov
#

from dropbox import users

from .test_engine import BaseCLITest


class TestAccountCommand(BaseCLITest):
    """
    Tests for dropme account related commands.
    """

    def test_account_info_show(self, mocker, mock_client, mock_dropbox):
        args = 'whoami'
        mock_client.users_get_current_account.return_value = users.FullAccount(
            name=users.Name(display_name='John Doe'),
            email='j.doe.example.com',
            country='UA')
        self.exec_command(args)

        mock_dropbox.assert_called_once_with(mocker.ANY)
        mock_client.users_get_current_account.assert_called_once_with()

    def test_space_usage_show(self, mocker, mock_client, mock_dropbox):
        used = 100
        allocated = 100000
        mock_client.users_get_space_usage.return_value = users.SpaceUsage(
            used=used,
            allocation=users.SpaceAllocation(
                'individual', users.IndividualSpaceAllocation(allocated)))
        args = 'df'
        self.exec_command(args)

        mock_dropbox.assert_called_once_with(mocker.ANY)
        mock_client.users_get_space_usage.assert_called_once_with()
