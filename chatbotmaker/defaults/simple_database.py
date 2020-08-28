""" SimpleDatabase class file"""
from . import Column, Integer, String, relationship, ForeignKey,\
              declarative_base, engine_from_config, sessionmaker
from ..database import create_user_class, create_argument_class


class SimpleDatabase:
    """ Database representation and basic user management """

    def __init__(self, config):
        self.config = config
        self.base = declarative_base()
        # Define default tables/classes here
        self.init_default_tables()
        self.engine = engine_from_config(self.config)
        # Create database if not exists here
        self.base.metadata.create_all(self.engine)
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)

    def init_default_tables(self):
        """ Initializes the default databases """
        self.user_class = create_user_class(self.base)
        self.argument_class = create_argument_class(self.base)
