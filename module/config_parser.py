import os
from configparser import ConfigParser


# parse config.ini contents with defined section
def any_config(filename=os.getcwd() + '/config.ini', section='bot'):
    parser = ConfigParser()
    parser.read(filename)
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return config


def get_games():
    config = any_config()
    frames = config['game_frames'].split(';')
    strategies = config['strategies'].split(';')
    if len(frames) is not len(strategies):
        quit('frames and strategies count do not match, check your config.ini')
    # for name, folder in zip(names, folders):
