from module import random_utils
import pyautogui
import random
import numpy as np
import time
from scipy import interpolate

# Any duration less than this is rounded to 0.0 to instantly move the mouse.
pyautogui.MINIMUM_DURATION = 0  # Default: 0.1
# Minimal number of seconds to sleep between mouse moves.
pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
# The number of seconds to pause after EVERY public function call.
pyautogui.PAUSE = 0  # Default: 0.1
# "PyAutoGUI fail-safe triggered from mouse moving to a corner of the screen.
# To disable this fail-safe, set pyautogui.FAILSAFE to False. DISABLING FAIL-SAFE IS NOT RECOMMENDED."
pyautogui.FAILSAFE = False


def random_mouse_move(target_x, target_y, rnd=500, duration=0.1):
    cp = random.randint(3, 5)  # Number of control points. Must be at least 2.
    x1, y1 = pyautogui.position()  # Starting position

    # Distribute control points between start and destination evenly.
    x = np.linspace(x1, target_x, num=cp, dtype='int')
    y = np.linspace(y1, target_y, num=cp, dtype='int')

    # Randomise inner points a bit (+-RND at most).
    xr = [random.randint(-rnd, rnd) for k in range(cp)]
    yr = [random.randint(-rnd, rnd) for k in range(cp)]
    xr[0] = yr[0] = xr[-1] = yr[-1] = 0
    x += xr
    y += yr

    # Approximate using Bezier spline.
    degree = 3 if cp > 3 else cp - 1  # Degree of b-spline. 3 is recommended.
    # Must be less than number of control points.
    tck, u = interpolate.splprep([x, y], k=degree)
    # Move upto a certain number of points
    u = np.linspace(0, 1, num=2 + int(random_utils.point_dist(x1, y1, target_x, target_y) / 50.0))
    points = interpolate.splev(u, tck)

    # Move mouse.
    timeout = duration / len(points[0])
    point_list = zip(*(i.astype(int) for i in points))
    for point in point_list:
        pyautogui.moveTo(*point)
        time.sleep(timeout)
