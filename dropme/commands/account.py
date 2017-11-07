#
#    Copyright 2017 Vitalii Kulanov
#

from cliff import show

from .base import BaseCommand
from ..common import utils


class AccountOwnerShow(show.ShowOne, BaseCommand):

    columns = ('User', 'e-mail', 'Country')

    def take_action(self, parsed_args):
        response = self.client.users_get_current_account()
        data = {
            'User': response.name.display_name,
            'e-mail': response.email,
            'Country': response.country
        }
        data = utils.get_display_data_single(self.columns, data)
        return self.columns, data


class AccountOwnerSpaceUsageShow(show.ShowOne, BaseCommand):

    columns = ('Allocated', 'Used', 'Available')

    def take_action(self, parsed_args):
        response = self.client.users_get_space_usage()
        allocated = response.allocation.get_individual().allocated
        used = response.used
        available = allocated - used
        data = {
            'Allocated': utils.convert_size(allocated),
            'Used': '{} ({:.3}%)'.format(utils.convert_size(used),
                                         available * 100 / allocated),
            'Available': utils.convert_size(available),
        }
        data = utils.get_display_data_single(self.columns, data)
        return self.columns, data
