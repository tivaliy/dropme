#
#    Copyright 2017 Vitalii Kulanov
#

import pytest

from dropme.common import utils


@pytest.mark.parametrize('data, file_name, expected', [
    ('---\nfake:\n  foo:\n  - bar\n', 'fake.yaml', {'fake': {'foo': ['bar']}}),
    ('', 'fake.yaml', {})
])
def test_read_from_yaml_file(data, file_name, expected, tmpdir):
    fake_file = tmpdir.join(file_name)
    fake_file.write(data)
    assert utils.read_yaml_file(fake_file.strpath) == expected


@pytest.mark.parametrize('example_input, expected_result', [
    (0, '0 B'),
    (1, '1.0 B'),
    (1056, '1.03 KB'),
    (20467, '19.99 KB'),
    (3405000, '3.25 MB'),
    (10203437400, '9.5 GB'),
    (5640003030040, '5.13 TB'),
    (4456703885093900, '3.96 PB'),
    (6788000399299490593, '5.89 EB'),
    (3242345678456005030405, '2.75 ZB'),
    (1002030103400102203040022, '848.75 ZB')
])
def test_convert_size(example_input, expected_result):
    assert utils.convert_size(example_input) == expected_result


@pytest.mark.parametrize('example_input, expected_error', [
    (-1, ValueError),
    ('45', TypeError),
])
def test_convert_size_w_wrong_parameters_fail(example_input, expected_error):
    with pytest.raises(expected_error):
        assert utils.convert_size(example_input)


@pytest.mark.parametrize('fields, data, missing_field_value, expected', [
    (('a', 'b', 'c'), {'a': 1, 'b': 2, 'c': 3}, None, [1, 2, 3]),
    (('a', 'b', 'c'), {'a': 1, 'b': 2, 'd': 3}, None, [1, 2, None]),
    (('a', 'b', 'c'), {'a': 1, 'b': 2, 'd': 3}, '-', [1, 2, '-']),
    (('a', 'b'), {'a': 1, 'b': 2, 'c': 3}, '-', [1, 2])
])
def test_get_display_data_single(fields, data, missing_field_value, expected):
    assert utils.get_display_data_single(fields,
                                         data,
                                         missing_field_value) == expected


@pytest.mark.parametrize('fields, data, sort_by, expected', [
    (('a', 'b'), [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}], None, [[1, 2], [3, 4]]),
    (('a', 'b'), [{'a': 1, 'b': 2}, {'a': 3}], None, [[1, 2], [3, None]]),
    (('a', 'b'), [{'a': 9, 'b': 7}, {'a': 3, 'b': 4}], 'b', [[3, 4], [9, 7]]),
    (('a', 'b'), [{'a': 9, 'b': 7}, {'a': 13, 'b': 1}], 'a', [[9, 7], [13, 1]])
])
def test_get_display_data_multi(fields, data, sort_by, expected):
    assert utils.get_display_data_multi(fields, data, sort_by) == expected


def test_get_display_data_multi_w_non_existing_sort_by_field():
    assert utils.get_display_data_multi(
        ('a', 'b'), [{'a': 12, 'b': 17}, {'a': 11, 'b': 5}], 'non-existing'
    ) == [[12, 17], [11, 5]]


@pytest.mark.parametrize('example_path, expected_result', [
    ('/foo/bar', '/foo/bar'),
    ('dummy/path', '/dummy/path'),
    ('path/contains/trailing/slash/', '/path/contains/trailing/slash/'),
])
def test_normalize_path(example_path, expected_result):
    assert utils.normalize_path(example_path) == expected_result
