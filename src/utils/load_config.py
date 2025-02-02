from pathlib import Path
import src.utils.general as utils

current_file_path = Path(__file__)
main_directory = current_file_path.parents[2]
config_path = main_directory.joinpath('src/utils/config.yml')

app_config = utils.read_yaml(config_path)
assert app_config is not None, 'The config dictionary could not be set'
