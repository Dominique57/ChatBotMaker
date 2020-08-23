# database imports
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
# app imports
from flask import Flask, request
from chatbotmaker import Bot, Dispatcher, Database
from chatbotmaker.defaults.dev import DevMessenger


engine = create_engine('sqlite:///foo.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    """ User class """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    fb_id = Column(String)
    state = Column(String)
    # Arguments (One to Many)
    arguments = relationship('Argument', back_populates='user', lazy='dynamic')

    def __init__(self, fb_id, state):
        self.fb_id = fb_id
        self.state = state

    def __repr__(self):
        return f'User: {self.fb_id}'


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


Base.metadata.create_all(engine)
dispatcher_config = {
    'actions': {
        'welcome': {
            'func': lambda user, user_input: (
                user.send_message('Im in welcome state'),
                user.change_state('home')
            )
        },
        'home': {
            'func': lambda user, user_input: (
                user.send_message('Im in home state'),
                user.change_state('welcome')
            )
        },
    }
}
messenger = DevMessenger()
dispatcher = Dispatcher(dispatcher_config)
database = Database(engine, Session, User, Argument)
bot = Bot({}, messenger, dispatcher, database)
FACEBOOK_CHECK_TOKEN = 'VERIFY_TOKEN'
app = Flask(__name__)


@app.route('/bot', methods=['GET', 'POST'])
def ngn_bot():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        token_resonse = request.args.get("hub.challenge")
        if token_sent == FACEBOOK_CHECK_TOKEN:
            return token_resonse
        return 'Invalid token_check'
    if request.method == 'POST':
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    recipient_id = message['sender']['id']
                    message = message['message'].get('text')
                    if message:
                        return bot.user_handle(recipient_id, message)
    return "Message ignored"


@app.route('/bot_debug', methods=['GET'])
def ngn_bot_debug():
    if request.method == 'GET':
        user_id = request.args.get("user")
        user_input = request.args.get("message")
        return bot.user_handle(user_id, user_input)
    return "Message ignored"


app.run()
