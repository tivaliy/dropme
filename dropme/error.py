#
#    Copyright 2017 Vitalii Kulanov
#


class ClientException(Exception):
    """Base Exception for Dropme client

    All child classes must be instantiated before raising.
    """
    pass


class ConfigNotFoundException(ClientException):
    """
    Should be raised if configuration for dropme client is not specified.
    """
    pass


class InvalidFileException(ClientException):
    """
    Should be raised when some problems while working with file occurred.
    """
    pass


class ActionException(ClientException):
    """
    Should be raised when some problems occurred while perform any command
    """
