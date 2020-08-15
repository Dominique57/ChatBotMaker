from . import Argument
"""
flow manages the user flow by creating handles in the handles dictionnary
"""


handles = {}


def create_handle(name, message=None, func_message=None, redir=None,
                  callback=None, arg_name=None, arg_check=None):
    """ creates a named handle for users to interact with """
    def func(user, user_input, session):
        """ Functional handle that will be stored in the module """
        if arg_name:
            if arg_check and not arg_check(user_input):
                print('User message does not conform')
                user.send_message('Message is in invalid format. Try again.')
                return
            else:
                print('User message conforms, saving to the server')
                # TODO: overwrite existing value
                argument = user.arguments.filter(
                               Argument.name == arg_name).scalar()
                if argument is None:
                    argument = Argument(name=arg_name, value=user_input)
                    user.arguments.append(argument)
                else:
                    argument.value = user_input
        if message:
            user.send_message(message)
        if func_message:
            user.send_message(str(func_message(user)))
        if redir:
            user.change_state(redir)
        if callback:
            callback(user)
    handles[name] = func
    handles[name] = func


create_handle('home', message='Main Page')
create_handle('help', message='Here are some useful commands', redir='home')
create_handle('name', message='What is your name?', redir='name_response')
create_handle('name_response',
              func_message=lambda user: f"Hi {user.get_argument('name')}",
              callback=lambda user: print(f'{user}'),
              arg_check=lambda text: len(text) >= 3,
              arg_name='name', redir='home')
