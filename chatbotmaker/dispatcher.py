""" Dispatcher class file """


def json_check(json_object: dict, key_name: str, optional=False,
               from_type=None, is_function=None):
    """ Checks wether a json object-key respects some rules """
    value = json_object.get(key_name)
    name = str(json_object)
    if value is None:
        if optional:
            return value
        raise Exception(f'{name} missing key: {key_name}')

    ext_name = name + ': ' + key_name
    if from_type and not isinstance(value, from_type):
        raise Exception(f'{ext_name} wrong type: expected {str(from_type)}')
    if is_function and not callable(value):
        raise Exception(f'{ext_name} not a function')
    return value


def initialize_from_function_name(state_name, env=None):
    """ Initializes a handle from its name and the environment it has
        been defined in"""
    if env is None:
        env = globals()
    result = {}
    optionals = ['pre_func', 'post_func']
    obligatorys = ['func']
    for optional in optionals:
        if (value := env.get(f'{optional}_{state_name}')) is not None:
            result[optional] = value
    for obligatory in obligatorys:
        result[obligatory] = env[f'{obligatory}_{state_name}']
    return result


class Dispatcher:
    """ Dispatchs function regarding user input """

    DEFAULT = object()

    def __init__(self, config: dict, env=None):
        self.config = config
        self.initialize_default_handles(env)
        self.check_config()

    def initialize_default_handles(self, env):
        """ Loads the DEFAULT handles from the env """
        action = self.config['actions']
        for name in action:
            if action[name] == self.DEFAULT:
                action[name] = initialize_from_function_name(name, env)

    def check_config(self):
        """ Check if config object is valid """
        actions = json_check(self.config, 'actions', from_type=dict)
        for name, action in actions.items():
            # check that action is a dict
            json_check(actions, name, from_type=dict)
            # check action content
            json_check(action, 'pre-func', optional=True, is_function=True)
            json_check(action, 'func', is_function=True)
            json_check(action, 'post-func', optional=True, is_function=True)

    def execute_pre_func(self, user):
        """ Executes the pre-call of a handle """
        action = self.config['actions'][user.state]
        if callback := action.get('pre_func'):
            callback(user)

    def execute_func(self, user, user_input: str):
        """ Executes the call of a handle """
        self.config['actions'][user.state]['func'](user, user_input)

    def execute_post_func(self, user):
        """ Executes the post-call of a handle """
        action = self.config['actions'][user.state]
        if callback := action.get('post_func'):
            callback(user)
