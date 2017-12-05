#
#    Copyright 2017 Vitalii Kulanov
#

import math
import os

import yaml


def read_yaml_file(file_path):
    """Parses yaml.

    :param file_path: path to yaml file as a string
    :returns: deserialized file
    """

    with open(file_path, 'r') as stream:
        data = yaml.safe_load(stream) or {}
    return data


def get_display_data_single(fields, data, missing_field_value=None):
    """Performs slicing of data by set of given fields.

    :param fields: Iterable containing names of fields to be retrieved
                   from data
    :param data:   Collection of objects representing some external entities
    :param missing_field_value: the value will be used for all missing fields

    :return:       List containing the collection of values of the
                   supplied attributes
    """

    return [data.get(field, missing_field_value) for field in fields]


def get_display_data_multi(fields, data, sort_by=None):
    """Performs slice of data by set of given fields for multiple objects.

    :param fields:  Iterable containing names of fields to be retrieved
                    from data
    :param data:    Collection of objects representing some external entities
    :param sort_by: List of fields to sort by. By default no sorting. Wrong
                    values are ignored
    :return:        List containing the collection of values of the
                    supplied attributes
    """

    data = [get_display_data_single(fields, elem) for elem in data]
    if sort_by:
        s_col_ids = [fields.index(col) for col in sort_by if col in fields]
        data.sort(key=lambda x: [x[s_col_id] for s_col_id in s_col_ids])
    return data


def convert_size(size_bytes):
    """
    Convert size in bytes to a human-readable form.
    """

    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "{} {}".format(s, size_name[i])


def normalize_path(path):
    """
    Normalize a pathname by adding leading slash
    """
    return path if path.startswith('/') else os.path.join('/', path)
