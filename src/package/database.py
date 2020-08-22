""" Database class file"""

class Database:
    """ Database representation (only show what exists) """
    def __init__(self, engine, session, user_class, argument_class):
        self.engine = engine
        self.session = session
        self.user_class = user_class
        self.argument_class = argument_class
