class Game(object):

    # Class constructor
    def __init__(self, x, y, x2, y2, strategy, state=1):
        self.x = x  # game window frame
        self.y = y  # game window frame
        self.x2 = x2  # game window frame
        self.y2 = y2  # game window frame
        self.strategy = strategy  # game strategy
        self.state = state

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
