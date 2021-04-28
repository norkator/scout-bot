import random
import math


# get random point for x and y pixel ranges
def random_point(x, y, x2, y2):
    x_ = int((x + x2) / 2)
    y_ = int((y + y2) / 2)
    r1 = random.randint(x_ - 5, x_ + 5)
    r2 = random.randint(y_ - 5, y_ + 5)
    return r1, r2


# mouse move helper
def point_dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
