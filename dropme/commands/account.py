#
#    Copyright 2017 Vitalii Kulanov
#

from .base import BaseShowCommand
from ..common import utils


class AccountOwnerInfoShow(BaseShowCommand):
    """
    Shows information about the current user's account.
    """

    columns = ('user', 'e_mail', 'country', 'account_type')

    @staticmethod
    def _get_account_type(account_type):
        account_type_mapper = {'basic': account_type.is_basic(),
                               'pro': account_type.is_pro(),
                               'business': account_type.is_business()}
        return next(k for k, v in account_type_mapper.items() if v)

    def get_parser(self, prog_name):
        parser = super(AccountOwnerInfoShow, self).get_parser(prog_name)
        parser.add_argument(
            '-a',
            '--all',
            action='store_true',
            help='Show information about account in more details.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.users_get_current_account()
        data = {
            'user': response.name.display_name,
            'e_mail': response.email,
            'country': response.country,
            'account_type': self._get_account_type(response.account_type),
        }
        if parsed_args.all:
            # TODO(vkulanov) Add more results
            self.columns += ('account_id', 'team', 'team_member_id')
            data.update({'account_id': response.account_id,
                         'team': response.team,
                         'team_member_id': response.team_member_id})
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
            'used': utils.convert_size(used),
            'available': '{} ({:.3}%)'.format(utils.convert_size(available),
                                              available * 100 / allocated)
        }
        data = utils.get_display_data_single(self.columns, data)
        return self.columns, data
