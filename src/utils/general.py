import yaml
from pathlib import Path


def read_yaml(file_path: Path) -> dict:
    """Read yaml files for general use.

    Args:
        file_path (Path): file path of yaml to read

    Raises:
        PermissionError: Raised if function does not have permission to access file
        IOError: Raised if file cannot be read
        Exception: General exception just in case

    Returns:
        dict: dictionary with yaml information or None if error occurs
        str: Logged information in form of Exception or string
    """
    try:
        with open(
            file=file_path,
            mode='r',
            encoding="utf-8"
        ) as file:
            yaml_dict = yaml.safe_load(file)
    except PermissionError as pe:
        raise PermissionError('Try closing out the file you are trying to read') from pe
    except IOError as io:
        raise IOError("Trouble reading yaml file") from io
    except Exception as e:
        raise Exception("An unknown error has occured") from e

    return yaml_dict
