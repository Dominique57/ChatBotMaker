from . import Column, String, Integer, ForeignKey, Table, relationship, Base,\
              engine
from . import bot

user_channel_association = Table(
    'users_channels', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('channel_id', Integer, ForeignKey('channels.id'))
)


class User(Base):
    """ User class """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    fb_id = Column(String)
    # STATE: could be better stored in a 1-1 relationship
    state = Column(String)
    # CHANNEL (Many to Many)
    channels = relationship('Channel', secondary=user_channel_association)
    # Arguments (One to Many)
    arguments = relationship('Argument', back_populates='user', lazy='dynamic')

    def __init__(self, fb_id, state):
        self.fb_id = fb_id
        self.state = state

    def __repr__(self):
        return f'User: {self.fb_id}'

    def change_state(self, state):
        """ Changes the state (ie. next function to be executed) of a user """
        self.state = state

    def send_message(self, message):
        bot.send_text_message(self.fb_id, message)

    def get_argument(self, name, default='None'):
        res = self.arguments.filter(Argument.name==name).scalar().value
        if res is None:
            return default
        return res


class Argument(Base):
    """ Argument class """
    __tablename__ = 'arguments'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(String)
    # User 1-Many relationship
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', uselist=False, back_populates='arguments')

    def __init__(self, name, value):
        self.name = name
        self.value = value


class Channel(Base):
    """ Channel class """
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # USER (Many to Many)
    users = relationship('User', secondary=user_channel_association)
    # SERVER (Channel - Many to One - Server)
    server_id = Column(Integer, ForeignKey('servers.id'))
    server = relationship('Server', uselist=False, back_populates='channels')

    def __init__(self, name, server):
        self.name = name
        self.server = server

    def __repr__(self):
        return f'Channel: {self.name} in {self.server.name}'


class Server(Base):
    """ Server class """
    __tablename__ = 'servers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    channels = relationship('Channel', back_populates='server')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        channels_name = [chan.name for chan in self.channels]
        return f'server: {self.name} ({", ".join(channels_name)})'


#  Creates database
Base.metadata.create_all(engine)
