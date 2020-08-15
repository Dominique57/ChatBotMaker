from ..config_loader import import_function, check_json
from . import pytest


valid_testdata = [
    ('def f(x): return x', 'f', (1, 1), (2, 2)),
    ('def f(x): return x + 10', 'f', (1, 11), (2, 12)),
    ('def g(x): return x.lower()', 'g', ('A', 'a'), ('AbC', 'abc')),
]


@pytest.mark.parametrize('fun,name,one,two', valid_testdata)
def test_import_valid_function_one_arg(fun, name, one, two):
    str_fun, str_name = fun, name
    success, res = import_function(str_fun, str_name, 1)
    assert success and callable(res)
    assert res(one[0]) == one[1] and res(two[0]) == two[1]


invalid_testdata = [
    ('def f(x): return return', 'f', 'invalid syntax', 1),
    ('def f(x): return x', 'f', '0 argument', 0),
    ('def f(): return "a"', 'f', '1 argument', 1),
    ('def f(x, y): return x + y', 'f', '3 argument', 3),
]


@pytest.mark.parametrize('fun,name,err_text,arg_count', invalid_testdata)
def test_import_function_invalid(fun, name, err_text, arg_count):
    str_fun, str_name = fun, name
    success, res = import_function(str_fun, str_name, arg_count)
    assert not success and isinstance(res, str)
    assert err_text in res.lower()


check_json_valid = [
    {'handles': [{'name': 'home'}]},
    {'handles': [{'name': 'home', 'redir': 'toto'},
                 {'name': 'toto', 'arg_name': 'name'},
                 {'name': 'test', 'callback': 'def callback(user): return 1'},
    ]},
]


@pytest.mark.parametrize('data', check_json_valid)
def test_valid_check_json(data):
    res = check_json(data)
    assert res is None


check_json_invalid_basic = [
    ({}, 'missing root'),
    ({'handles': 'a'}, 'not a list'),
    ({'handles': []}, 'empty list'),
    ({'handles': ['a']}, 'not a dictionnary'),
    ({'handles': [{'not_name': 'home'}]}, 'has no name attribute'),
    ({'handles': [{'name': 'home'}, 'a']}, 'not a dictionnary'),
    ({'handles': [{'name': 'home'}, {'name': 'home'}]}, 'existing name'),
    ({'handles': [{'name': 'toto'}, {'name': 'tata'}]}, 'missing home'),
    ({'handles': [{'name': 'toto'}]}, 'missing home'),
]


@pytest.mark.parametrize('data,err_txt', check_json_invalid_basic)
def test_invalid_check_json_basic(data, err_txt):
    res = check_json(data)
    assert isinstance(res, str)
    assert err_txt in res.lower()


check_json_invalid_advanced = [
    ([{'name': 10}], 'isnt string'),
    ([{'message': 42}], 'isnt string'),
    ([{'redir': 69}], 'isnt string'),
    ([{'arg_name': 12}], 'isnt string'),
    ([{'invalid_arg': 12}], 'invalid key'),
    ([{'func_message': 'lambda user: return return'}], 'import failed'),
    ([{'callback': 'lambda user: return return'}], 'import failed'),
    ([{'arg_check': 'lambda text: return return'}], 'import failed'),
    ([{'redir': 'invalid_redir'}], 'invalid redirection'),
]


@pytest.mark.parametrize('data,err_txt', check_json_invalid_advanced)
def test_invalid_check_json_advanced(data, err_txt):
    i = 0
    for dic in data:
        if dic.get('name') is None:
            dic['name'], i = 'default_' + str(i), i + 1
    data = [{'name': 'home'}] + data
    data = {'handles': data}
    res = check_json(data)
    assert isinstance(res, str)
    assert err_txt in res.lower()
