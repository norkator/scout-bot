from module import config_parser
from strategy import scout
# import keyboard
import time
import sys

games = config_parser.get_games()


def run_app():
    for game in games:
        # if keyboard.is_pressed('p'):
        #     print('paused game ' + game.get_game_name())
        #     game.set_paused(True)
        #     time.sleep(2)
        # elif keyboard.is_pressed('r'):
        #     print('resume game ' + game.get_game_name())
        #     game.set_paused(False)
        #     time.sleep(2)
        if game.strategy == 'scout':
            if game.get_paused() is False:
                scout.scout(game)
        elif game.strategy == 'scout_test':
            scout.scout_test(game)
            sys.exit(0)
        else:
            print('no strategy for ' + game.strategy)


if __name__ == '__main__':
    try:
        while 1:
            run_app()
            time.sleep(0.5)
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)
