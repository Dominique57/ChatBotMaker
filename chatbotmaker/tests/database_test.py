from ..database import Database, create_user_class, create_argument_class
from .. import declarative_base, Column, Integer
from . import pytest


@pytest.mark.parametrize('generator,name,attributes', [
    (create_user_class, 'users', ['id', 'fb_id', 'state', 'arguments']),
    (create_argument_class, 'arguments', ['id', 'name', 'value', 'user_id',
                                          'user']),
])
def test_create_user_class(generator, name, attributes):
    base = declarative_base()
    # When
    User = generator(base)
    # Then
    assert User.__dict__.get('__tablename__') == name
    for attribute in attributes:
        assert attribute in User.__dict__.keys()
