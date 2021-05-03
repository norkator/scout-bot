from module import template_matcher, frame_capture, move_mouse, random_utils
import pyautogui
import time
import sys
import os

# scout states
STATE_BEGINNING = 0
STATE_CLICK_BOARD = 1
STATE_MAKE_PARTY = 2
CAVE_MARKER = 3
ENTER_CAVE = 4
KILL_PROCESS = 666


def check_cave_enter_failure(game):
    window_frame = frame_capture.capture_window_frame(game.x, game.y, game.x2, game.y2, im_show=False)
    ef = template_matcher.feature_matcher(window_frame, 'failed_party.png')
    if ef[0] is 107 and ef[1] is 364:
        return True
    else:
        return False


def home_point_1(game):
    window_frame = frame_capture.capture_window_frame(game.x, game.y, game.x2, game.y2, im_show=False)
    tp = template_matcher.feature_matcher(window_frame, 'home_point_1.png')
    target_offset_x, target_offset_y = random_utils.random_point(
        tp[0] + game.x, tp[1] + game.y, tp[2] + game.x, tp[3] + game.y
    )
    move_mouse.random_mouse_move(target_offset_x, target_offset_y, rnd=400, duration=0.5)
    pyautogui.click()
    time.sleep(5)
    print('not implemented right home point yet')
    game.__setstate__(KILL_PROCESS)


def scout(game):
    # window frame capture
    window_frame = frame_capture.capture_window_frame(game.x, game.y, game.x2, game.y2, im_show=False)

    if game.get_state() is STATE_BEGINNING:
        # compass detection
        tp = template_matcher.feature_matcher(window_frame, 'compass.png')

        # get randomised clicking point
        target_offset_x, target_offset_y = random_utils.random_point(
            tp[0] + game.x, tp[1] + game.y, tp[2] + game.x, tp[3] + game.y
        )

        # move mouse
        move_mouse.random_mouse_move(target_offset_x, target_offset_y, rnd=400, duration=0.5)
        pyautogui.click()  # pyautogui.moveTo(compass_points[0] + 20, compass_points[1] + 100, 4)

        game.__setstate__(STATE_CLICK_BOARD)

    elif game.get_state() is STATE_CLICK_BOARD:
        tp = template_matcher.feature_matcher(window_frame, 'board.png')

        # get randomised clicking point
        target_offset_x, target_offset_y = random_utils.random_point(
            tp[0] + game.x, tp[1] + game.y, tp[2] + game.x, tp[3] + game.y
        )

        # move mouse
        move_mouse.random_mouse_move(target_offset_x, target_offset_y, rnd=400, duration=0.5)
        pyautogui.click()

        game.__setstate__(STATE_MAKE_PARTY)


    elif game.get_state() is STATE_MAKE_PARTY:
        tp = template_matcher.feature_matcher(window_frame, 'make_party.png')

        # get randomised clicking point
        target_offset_x, target_offset_y = random_utils.random_point(
            tp[0] + game.x, tp[1] + game.y, tp[2] + game.x, tp[3] + game.y
        )

        # move mouse
        move_mouse.random_mouse_move(target_offset_x, target_offset_y, rnd=400, duration=0.5)
        pyautogui.click()

        # esc out from dialog
        # pyautogui.press('esc')
        # time.sleep(2)
        game.__setstate__(CAVE_MARKER)

    elif game.get_state() is CAVE_MARKER:
        tp = template_matcher.feature_matcher(window_frame, 'target_point.png')

        # get randomised clicking point
        target_offset_x, target_offset_y = random_utils.random_point(
            tp[0] + game.x, tp[1] + game.y, tp[2] + game.x, tp[3] + game.y
        )

        # move mouse
        move_mouse.random_mouse_move(target_offset_x, target_offset_y, rnd=400, duration=0.5)
        pyautogui.click()

        time.sleep(6)
        game.__setstate__(ENTER_CAVE)

    elif game.get_state() is ENTER_CAVE:
        tp = template_matcher.feature_matcher(window_frame, 'cave_entrance.png')

        # get randomised clicking point
        target_offset_x, target_offset_y = random_utils.random_point(
            tp[0] + game.x, tp[1] + game.y, tp[2] + game.x, tp[3] + game.y
        )

        # move mouse
        move_mouse.random_mouse_move(target_offset_x, target_offset_y, rnd=400, duration=0.5)
        pyautogui.click()

        time.sleep(2)
        if check_cave_enter_failure(game):
            home_point_1(game)
        else:
            game.__setstate__(KILL_PROCESS)


    elif game.get_state() is KILL_PROCESS:
        sys.exit(0)


# test scout vie finding specific object
def scout_test(game):
    # window frame capture
    window_frame = frame_capture.capture_window_frame(game.x, game.y, game.x2, game.y2, im_show=False)

    # compass detection test
    # template_matcher.feature_matcher(window_frame, 'compass.png', plot=True)

    # board detection test
    # template_matcher.feature_matcher(window_frame, 'board.png', plot=True)

    # failed party
    # template_matcher.feature_matcher(window_frame, 'failed_party.png', plot=True)
    # 107, 364, 402, 403

    # home point 1
    template_matcher.feature_matcher(window_frame, 'home_point_1.png', plot=True)
