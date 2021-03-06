from module import time_utils


class Game(object):

    # Class constructor
    def __init__(self, x, y, x2, y2, strategy, game_name, state=1):
        self.x = x  # game window frame
        self.y = y  # game window frame
        self.x2 = x2  # game window frame
        self.y2 = y2  # game window frame
        self.game_name = game_name
        self.strategy = strategy  # game strategy
        self.state = state
        self.paused = False
        self.sleep_millis = 0

    def print_game(self):
        print(self.x, self.y, self.x2, self.y2, self.strategy)

    def is_none(self):
        return self.x is None

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_x2(self):
        return self.x2

    def get_y2(self):
        return self.y2

    def get_state(self):
        return self.state

    def __setstate__(self, state):
        self.state = state

    def get_game_name(self):
        return self.game_name

    def set_paused(self, paused):
        self.paused = paused

    def get_paused(self):
        return self.paused

    def reset_state(self):
        self.state = 1

    def is_sleeping(self):
        current = time_utils.current_millis_time()
        if self.sleep_millis is not 0 and current > self.sleep_millis:
            self.sleep_millis = 0
        return self.sleep_millis is not 0

    def set_sleep(self, seconds):
        m = time_utils.current_millis_time()
        self.sleep_millis = m + (seconds * 1000)

    def get_sleep_millis(self):
        return self.sleep_millis
