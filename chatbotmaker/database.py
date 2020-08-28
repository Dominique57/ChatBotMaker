""" Database class file"""
from . import Column, Integer, String, relationship, ForeignKey


def create_user_class(base):
    """ Creates a User class with the given relationships """
    class User(base):
        """ User class """
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        fb_id = Column(String)
        state = Column(String)
        # Arguments (One to Many)
        arguments = relationship('Argument', back_populates='user',
                                 lazy='dynamic')

        def __init__(self, fb_id, state):
            self.fb_id = fb_id
            self.state = state

    return User


def create_argument_class(base):
    """ Creates a Argument class with the given relationships """
    class Argument(base):
        """ Argument class """
        __tablename__ = 'arguments'

        id = Column(Integer, primary_key=True)
        name = Column(String)
        value = Column(String)
        # User 1-Many relationship
        user_id = Column(Integer, ForeignKey('users.id'))
        user = relationship('User', uselist=False,
                            back_populates='arguments')

    return Argument


class Database:
    """ Database representation (only show what exists) """
    def __init__(self, engine, session, user_class, argument_class):
        self.engine = engine
        self.session = session
        self.user_class = user_class
        self.argument_class = argument_class
