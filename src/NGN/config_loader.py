from . import json, inspect, create_handle, nntplib, socket, Argument


def import_function(function_string, function_name, arg_count):
    try:
        locals()[function_name] = None
        exec(function_string)
        result_function = locals()[function_name]
        if result_function is None:
            raise Exception('Function has incorrect name')
        param_length = len(inspect.signature(result_function).parameters)
        if arg_count not in (-1, param_length):
            raise Exception(f'Function does not have {arg_count} argument(s)')
        return True, result_function
    except Exception as E:
        return False, str(E)


def check_json(data):
    handles_set = set()
    # Check root data structure / types
    if data.get('handles') is None:
        return 'missing root "handles" object'
    if not isinstance(data['handles'], list):
        return '"handles" object is not a list'
    if len(data['handles']) == 0:
        return '"handles" object is an empty list'
    # Check  all handles type and that they are named and store all names
    for handle in data['handles']:
        if not isinstance(handle, dict):
            return f'handle: {handle} is not a dictionnary object'
        if handle.get('name') is None:
            return f'handle: {handle} has no name attribute'
        if handle['name'] in handles_set:
            return f'handle: {handle} defines existing name {handle["name"]}'
        handles_set.add(handle["name"])
    # Check if a 'welcome' handle exists
    if 'welcome' not in handles_set:
        return 'Missing welcome handle!'
    # Check handle values now
    for handle in data['handles']:
        for key, value in handle.items():
            if key in ('name', 'message', 'redir', 'arg_name'):
                if not isinstance(value, str):
                    return f'handle: {handle} key: {key} - value isnt string'
            elif key in ('func_message', 'arg_check', 'callback'):
                success, res = import_function(value, key, -1)
                if not success:
                    return f'Function import failed: details: {res}'
            else:
                return f'Invalid key in {handle["name"]} handle: {key}'
            if key == 'redir':
                if value not in handles_set:
                    return f'handle: {handle} Invalid redirection: {value}'


def convert_json_to_handles(data):
    for handle in data['handles']:
        for key in handle.keys():
            if key in ('func_message', 'callback', 'arg_check'):
                success, res = import_function(handle[key], key, -1)
                handle[key] = res
        create_handle(**handle)


def decode_json(raw_data):
    data = json.loads(raw_data)
    error = check_json(data)
    if error:
        print(f'Error during parsing of bot:\n{error}')
        exit()
    convert_json_to_handles(data)


json_data = {'handles': [
    {'name': 'welcome', 'message': 'Hi there, press any command or "help" for more information!', 'redir': 'home'},
    {'name': 'home',
      'message': 'Invalid command, press "help" for more information!'},
    {'name': 'help',
      'message': 'Following commands are supported:\n - subscribe: subscribes to a NTP channel\n - unsubscribe: unsubscribes to a NTP channel subscription',
      'redir': 'home'},

    {'name': 'subscribe',
      'message': 'Please specify the server you want to subscribe to:',
      'redir': 'sub_ask_server'},
    {'name': 'sub_ask_server', 'arg_name': 'server_address',
      'arg_check': 'def arg_check(user, text):\n    try:\n        nntplib.NNTP(text)\n    except Exception:\n        return False\n    return True',
      'callback': 'def callback(user): user.send_message(\'Please specify the channel you want to subscribe to:\')',
      'redir': 'sub_ask_channel'},
    {'name': 'sub_ask_channel', 'arg_name': 'channel_name',
      'arg_check': 'def arg_check(user, text):\n    try:\n        s = user.arguments.filter(Argument.name == \'server_address\').scalar()\n        server = nntplib.NNTP(s.value)\n    except Exception:\n        user.send_message(\'Server argument became invalid! You will be directed to home page after error message!\')\n        user.change_state(\'home\')\n    try:\n        server.group(text)\n    except Exception:\n        return False\n    return True',
      'callback': 'def callback(user): user.send_message(\'Subscription saved!\')',
      'redir': 'home'},
    {'name': 'unsubscribe'},
    {'name': 'list_sub'},
    {'name': 'unsub_ask_confirmation'},
]}


decode_json(json.dumps(json_data))
