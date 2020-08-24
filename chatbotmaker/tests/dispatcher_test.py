from ..dispatcher import json_check, Dispatcher
from . import pytest


invalid_missing_jsoncheck = [
    ({}, 'data'),
    ({'nope': 42}, 'data'),
]


@pytest.mark.parametrize('json,key', invalid_missing_jsoncheck)
def test_json_invalid_missing(json, key):
    with pytest.raises(Exception) as exception_info:
        json_check(json, key)
    assert 'missing key' in str(exception_info)


invalid_type_jsoncheck = [
    ('value', int),
    (1, float),
    (1.2, list),
    ([1], dict),
    ({'a': 'b'}, str),
]


@pytest.mark.parametrize('value,type', invalid_type_jsoncheck)
def test_json_invalid_type(value, type):
    json = {'data': value}
    with pytest.raises(Exception) as exception_info:
        json_check(json, 'data', from_type=type)
    assert 'wrong type' in str(exception_info)


def test_json_invalid_type_function():
    json = {'data': 'not_func'}
    with pytest.raises(Exception) as exception_info:
        json_check(json, 'data', is_function=True)
    assert 'not a function' in str(exception_info)


valid_optional_jsoncheck = [
    ({'hi': 'there'}, 'ho'),
    ({'hi': 'there'}, 'hi'),
]


@pytest.mark.parametrize('json,key', valid_optional_jsoncheck)
def test_json_valid_optional(json, key):
    res = json_check(json, key, optional=True)
    assert res == json.get(key)


invalid_optional_jsoncheck = [
    ({'hi': 'there'}, 'hi', 'wrong type', {'from_type': int}),
    ({'hi': 42}, 'hi', 'wrong type', {'from_type': str}),
]


@pytest.mark.parametrize('json,key,error,args', invalid_optional_jsoncheck)
def test_json_invalid_optional(json, key, error, args):
    with pytest.raises(Exception) as exception_info:
        json_check(json, key, optional=True, **args)
    assert error in str(exception_info)
