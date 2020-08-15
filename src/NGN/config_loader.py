from . import json, inspect


def import_function(function_string, function_name, arg_count):
    try:
        locals()[function_name] = None
        exec(function_string)
        result_function = locals()[function_name]
        locals()[function_name] = None
        if len(inspect.signature(result_function).parameters) != arg_count:
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
    # Check if a 'home' handle exists
    if 'home' not in handles_set:
        return 'Missing home handle!'
    # Check handle values now
    for handle in data['handles']:
        for key, value in handle.items():
            if key in ('name', 'message', 'redir', 'arg_name'):
                if not isinstance(value, str):
                    return f'handle: {handle} key: {key} - value isnt string'
            elif key in ('func_message', 'callback', 'arg_check'):
                success, res = import_function(value, key, 1)
                if not success:
                    return f'Function import failed: details: {res}'
            else:
                return f'Invalid key in {handle["name"]} handle: {key}'
            if key == 'redir':
                if value not in handles_set:
                    return f'handle: {handle} Invalid redirection: {value}'

def convert_json_to_handles(data):
    return {}

def decode_json(raw_data):
    data = json.loads(raw_data)
    check_json(data)
    handles = convert_json_to_handles(data)
    return handles
