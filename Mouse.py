"""
Use this util to get window left top and right bottom corner pixel points
"""
import pyautogui
import time
import sys


def app():
    while 1:
        print(pyautogui.position())
        time.sleep(0.5)


if __name__ == '__main__':
    try:
        app()
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)
