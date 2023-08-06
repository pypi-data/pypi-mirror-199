import os
import re
from importlib.util import spec_from_file_location, module_from_spec
from types import ModuleType


def import_config_file(config_file: str) -> ModuleType:
    """Imports a module from it's file path.

    Args:
        config_file (str): The python file absolute path.

    Raises:
        FileNotFoundError: The python file does not exist at the specified location.

    Returns:
        ModuleType: The imported python module.
    """

    if not os.path.exists(config_file):
        raise FileNotFoundError(f'Python module at: {config_file} not found.')

    spec = spec_from_file_location('config_file', config_file)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def get_config(config_file: str, keys: list[str] = list()) -> dict[str]:
    """Retrieves the configuration from a python file and the environment.

    Args:
        config_file (str): The .py config file path.
        keys (list[str], optional): Name of variable to look for in the config file and in the environment. If not provided the keys will be retrived from the constants present in the config file.

    Raises:
        FileNotFoundError: The config file does not exist
        ValueError: A key is containing other characters than capital letters and underscores.

    Returns:
        dict[str]: A dictionnary containing the configuration merged from the config file and overriden by the environment.
    """

    # Check if the config file exists and import it as a module.
    config_file = os.path.abspath(config_file)

    if not os.path.exists(config_file):
        raise FileNotFoundError(
            f'config file at: {config_file} does not exists')

    config_mod: ModuleType = import_config_file(config_file)

    # Check key values.
    # If not keys specified use the constant existing in the config file.
    PATTERN: str = r"^[A-Z_]*$"

    if not keys:
        for d in dir(config_mod):
            if not d.startswith('__') and bool(re.match(PATTERN, d)):
                keys.append(d)

    else:
        for key in keys:
            if not bool(re.match(PATTERN, key)):
                raise ValueError(
                    f'Key {key} does not contain only capital letters and underscores')

    # Make the config dict.
    config: dict[str] = {}

    for key in keys:

        if not os.environ.get(key) == None:
            value = os.environ.get(key)

            if os.pathsep in value:
                file_value: list[str] = getattr(config_mod, key)

                values: list[str] = value.split(os.pathsep)

                value = values + file_value

        else:
            value = getattr(config_mod, key)

        config[key] = value

    return config
