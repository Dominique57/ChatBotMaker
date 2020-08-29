""" Database class file"""
from . import Column, Integer, String, relationship, ForeignKey,\
              declarative_base, engine_from_config, sessionmaker
from . import ExtendedUser


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
            self.extended = None

        def __getattr__(self, name):
            # gettatribute avoids recursion calling gettattr again
            if self.__getattribute__('extended') is not None:
                return getattr(self.extended, name)
            return getattr(self, name)

        def extend_user(self, messenger, dispatcher, database):
            """ Add sugar calling methods """
            self.extended = ExtendedUser(self, messenger, dispatcher, database)

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

        def __init__(self, name, value):
            self.name = name
            self.value = value

    return Argument


class Database:
    """ Database representation (only show what exists) """

    def __init__(self, config, create_database=True):
        self.base = declarative_base()
        self.init_default_tables()
        self.engine = engine_from_config(config)
        if create_database:
            self.create_database()

    def init_default_tables(self):
        """ Initializes the default classes/tables """
        self.user_class = create_user_class(self.base)
        self.argument_class = create_argument_class(self.base)

    def create_database(self):
        """ Creates the database and end the final initialisation """
        self.base.metadata.create_all(self.engine)
        self.session_maker = sessionmaker()
        self.session_maker.configure(bind=self.engine)
