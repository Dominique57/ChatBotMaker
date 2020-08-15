from . import Argument
"""
flow manages the user flow by creating handles in the handles dictionnary
"""


handles = {}


def create_handle(name, message=None, func_message=None, redir=None,
                  callback=None, arg_name=None, arg_check=None):
    """ creates a named handle for users to interact with """
    def func(user, user_input):
        """ Functional handle that will be stored in the module """
        user.mark_seen()
        if message or func_message:
            user.mark_writing()

        if arg_name:
            if arg_check and not arg_check(user_input):
                user.send_message('Message is in invalid format. Try again.')
                return
            else:
                argument = user.arguments.filter(Argument.name == arg_name)\
                                         .scalar()
                if argument is None:
                    argument = Argument(name=arg_name, value=user_input)
                    user.arguments.append(argument)
                else:
                    argument.value = user_input
        if message:
            user.send_message(message)
        if func_message:
            user.send_message(str(func_message(user)))
        if message or func_message:
            user.mark_writing(False)
        if redir:
            user.change_state(redir)
        if callback:
            callback(user)
    handles[name] = func
    return func
