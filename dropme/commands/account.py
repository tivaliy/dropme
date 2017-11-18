#
#    Copyright 2017 Vitalii Kulanov
#

from .base import BaseShowCommand
from ..common import utils


class AccountOwnerInfoShow(BaseShowCommand):
    """
    Shows information about the current user's account.
    """

    columns = ('user', 'e_mail', 'country')

    def get_parser(self, prog_name):
        parser = super(AccountOwnerInfoShow, self).get_parser(prog_name)
        parser.add_argument(
            '-a',
            '--all',
            action='store_true',
            help='show information about account in more details'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.users_get_current_account()
        data = {
            'user': response.name.display_name,
            'e_mail': response.email,
            'country': response.country,
        }
        if parsed_args.all:
            # TODO(vkulanov) Add more results
            self.columns += ('account_id', 'team', 'team_member_id')
            data['account_id'] = response.account_id
            data['team'] = response.team
            data['team_member_id'] = response.team_member_id
        data = utils.get_display_data_single(self.columns, data)
        return self.columns, data


class AccountOwnerSpaceUsageShow(BaseShowCommand):
    """
    Shows information about space usage of the current user's account.
    """

    columns = ('allocated', 'used', 'available')

    def take_action(self, parsed_args):
        response = self.client.users_get_space_usage()

        allocated = response.allocation.get_individual().allocated
        used = response.used
        available = allocated - used
        data = {
            'allocated': utils.convert_size(allocated),
            'used': '{} ({:.3}%)'.format(utils.convert_size(used),
                                         available * 100 / allocated),
            'available': utils.convert_size(available),
        }
        data = utils.get_display_data_single(self.columns, data)
        return self.columns, data
