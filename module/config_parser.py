from configparser import ConfigParser
from objects import game
import os


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
    games = []
    config = any_config()
    frames = config['game_frames'].split(';')
    strategies = config['strategies'].split(';')
    names = config['game_names'].split(';')
    if len(frames) is not len(strategies):
        quit('frames and strategies count do not match, check your config.ini')
    for frame, strategy, name in zip(frames, strategies, names):
        frame_ = frame.split(',')
        try:
            game_ = game.Game(
                int(frame_[0]),
                int(frame_[1]),
                int(frame_[2]),
                int(frame_[3]),
                strategy,
                name
            )
            if game_.is_none() is not None:
                games.append(game_)
        except ValueError as e:
            pass
    return games
