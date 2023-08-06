import os


def get_env(name):
    """
    Get environment variable value by name
    :param name: environment variable name
    :return: environment variable value
    """
    value = os.getenv(name)
    if value is not None:
        return value
    raise Exception(f'No environment variable: {name}')
