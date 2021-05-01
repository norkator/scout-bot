from module import frame_capture, color_utils
import pyautogui
import random
import time

tool = [899, 610, 926, 656]  # fishing tool bottom position
p = 1200
p2 = 1022

# Any duration less than this is rounded to 0.0 to instantly move the mouse.
# pyautogui.MINIMUM_DURATION = 0  # Default: 0.1
# Minimal number of seconds to sleep between mouse moves.
# pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
# The number of seconds to pause after EVERY public function call.
# pyautogui.PAUSE = 0  # Default: 0.1

# window frame capture
while 1:
    window_frame = frame_capture.capture_window_frame_continuous(tool[0], tool[1], tool[2], tool[3], im_show=False)
    avg_color = color_utils.get_avg_color(window_frame)
    if avg_color < 160:
        print('FISH!')
        # pyautogui.moveTo(x=1082, y=968)
        pyautogui.moveTo(x=p, y=p2)
        pyautogui.dragTo(x=p, y=p2 - 100, duration=0.2, button='left')  # focus the window
        pyautogui.moveTo(x=p, y=p2)
        # pyautogui.click(1082, 882, button='left')  # simulate left click
        time.sleep(2)

        # pyautogui.dragTo(x=1082, y=882, duration=0.2)
        # pyautogui.moveTo(x=1082, y=968)
        # pyautogui.click()
        # pyautogui.dragTo(1082, 882, 0.2, button='left')
        # 1082, y = 968
        # 1082, y = 882)
    elif random.randint(0, 400) is 18:
        print('Random swing')
        pyautogui.moveTo(x=p, y=p2)
        pyautogui.dragTo(x=p, y=p2 - 100, duration=0.2, button='left')  # focus the window
        pyautogui.moveTo(x=p, y=p2)
        time.sleep(2)
