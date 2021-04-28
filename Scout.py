from module import config_parser
from strategy import scout
import time
import sys

games = config_parser.get_games()


def run_app():
    for game in games:
        if game.strategy == 'scout':
            scout.scout(game)
        else:
            print('no strategy for ' + game.strategy)


if __name__ == '__main__':
    try:
        while 1:
            run_app()
            time.sleep(1.0)
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)
