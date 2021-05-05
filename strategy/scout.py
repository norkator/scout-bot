from module import template_matcher, frame_capture, move_mouse, random_utils
from playsound import playsound
import pyautogui
import time
import sys
import os

# scout states
STATE_NONE = 0
STATE_BEGINNING = 1
STATE_CLICK_BOARD = 2
STATE_MAKE_PARTY = 3
STATE_CAVE_MARKER = 4
STATE_ENTER_CAVE = 5
STATE_IN_CAVE = 8
STATE_CAVE_DETECT_OPTIMAL_RAID = 9
STATE_CAVE_ALARM = 10
STATE_CAVE_EXIT = 11
STATE_CAVE_FINISHED = 11
KILL_PROCESS = 666

OPTIMAL_RAIDS = [
    'raid_1.png'
]


def scout(game):
    # window frame capture
    window_frame = frame_capture.capture_window_frame(game.x, game.y, game.x2, game.y2, im_show=False)

    if game.get_state() is STATE_BEGINNING:
        tp = template_matcher.feature_matcher(window_frame, 'compass.png', game)
        target_offset_x, target_offset_y = random_utils.random_point(
            tp[0] + game.x, tp[1] + game.y, tp[2] + game.x, tp[3] + game.y
        )
        move_mouse.random_mouse_move(target_offset_x, target_offset_y, rnd=400, duration=0.5)
        pyautogui.click()
        game.__setstate__(STATE_CLICK_BOARD)

    elif game.get_state() is STATE_CLICK_BOARD:
        tp = template_matcher.feature_matcher(window_frame, 'board.png', game)
        target_offset_x, target_offset_y = random_utils.random_point(
            tp[0] + game.x, tp[1] + game.y, tp[2] + game.x, tp[3] + game.y
        )
        move_mouse.random_mouse_move(target_offset_x, target_offset_y, rnd=400, duration=0.5)
        pyautogui.click()
        time.sleep(2)
        game.__setstate__(STATE_MAKE_PARTY)

    elif game.get_state() is STATE_MAKE_PARTY:
        tp = template_matcher.feature_matcher(window_frame, 'make_party.png', game)
        target_offset_x, target_offset_y = random_utils.random_point(
            tp[0] + game.x, tp[1] + game.y, tp[2] + game.x, tp[3] + game.y
        )
        move_mouse.random_mouse_move(target_offset_x, target_offset_y, rnd=400, duration=0.5)
        pyautogui.click()

        # esc out from dialog
        # pyautogui.press('esc')
        time.sleep(1)
        game.__setstate__(STATE_CAVE_MARKER)

    elif game.get_state() is STATE_CAVE_MARKER:
        tp = template_matcher.feature_matcher(window_frame, 'target_point.png', game)
        target_offset_x, target_offset_y = random_utils.random_point(
            tp[0] + game.x, tp[1] + game.y, tp[2] + game.x, tp[3] + game.y
        )
        move_mouse.random_mouse_move(target_offset_x, target_offset_y, rnd=400, duration=0.5)
        pyautogui.click()

        time.sleep(6)
        game.__setstate__(STATE_ENTER_CAVE)

    elif game.get_state() is STATE_ENTER_CAVE:
        tp = template_matcher.feature_matcher(window_frame, 'cave_entrance.png', game)
        target_offset_x, target_offset_y = random_utils.random_point(
            tp[0] + game.x, tp[1] + game.y, tp[2] + game.x, tp[3] + game.y
        )
        move_mouse.random_mouse_move(target_offset_x, target_offset_y, rnd=400, duration=0.5)
        pyautogui.click()

        time.sleep(2)
        if cave_enter_success(game) is False:
            home_point_1(game)
        else:
            game.__setstate__(STATE_IN_CAVE)

    elif game.get_state() is STATE_IN_CAVE:
        print('[' + game.get_game_name() + '][' + str(game.get_state()) + '] We have entered in the cave')
        game.__setstate__(STATE_CAVE_DETECT_OPTIMAL_RAID)

    elif game.get_state() is STATE_CAVE_DETECT_OPTIMAL_RAID:
        match_found = template_matcher.feature_matcher_match_found(
            window_frame, 'find_raid', OPTIMAL_RAIDS, game, plot=True
        )
        if match_found is True:
            game.__setstate__(STATE_CAVE_ALARM)
        else:
            game.__setstate__(STATE_CAVE_EXIT)

    elif game.get_state() is STATE_CAVE_EXIT:
        # this tries to calculate position to leave cave
        x_p = int(((game.x2 / 2) + game.x) * 60 / 100)
        y_p = int(((game.y2 / 2) + game.y) * 99 / 100)
        move_mouse.random_mouse_move(x_p, y_p, rnd=400, duration=0.5)
        pyautogui.click()
        time.sleep(2)
        window_frame = frame_capture.capture_window_frame(game.x, game.y, game.x2, game.y2, im_show=False)
        tp = template_matcher.feature_matcher(window_frame, 'leave_cave.png', game)
        target_offset_x, target_offset_y = random_utils.random_point(
            tp[0] + game.x, tp[1] + game.y, tp[2] + game.x, tp[3] + game.y
        )
        move_mouse.random_mouse_move(target_offset_x, target_offset_y, rnd=400, duration=0.5)
        pyautogui.click()
        print('[' + game.get_game_name() + '][' + str(game.get_state()) + '] exiting cave')
        time.sleep(5)
        game.__setstate__(STATE_BEGINNING)

    elif game.get_state() is STATE_CAVE_ALARM:
        bell = os.getcwd() + '/sounds/' + 'bell.wav'
        playsound(bell)
        playsound(bell)
        playsound(bell)
        alert = os.getcwd() + '/sounds/' + 'alert.wav'
        playsound(alert)
        game.__setstate__(STATE_CAVE_FINISHED)

    elif game.get_state() is STATE_CAVE_FINISHED:
        print('this window is in finished state')
        # Todo, maybe ad key to reset this?

    elif game.get_state() is KILL_PROCESS:
        sys.exit(0)


# test scout vie finding specific object
def scout_test(game):
    # window frame capture
    window_frame = frame_capture.capture_window_frame(game.x, game.y, game.x2, game.y2, im_show=False)

    # compass detection test
    # template_matcher.feature_matcher(window_frame, 'compass.png', game, plot=True)

    # board detection test
    # template_matcher.feature_matcher(window_frame, 'board.png', game, plot=True)

    # failed party
    # template_matcher.feature_matcher(window_frame, 'failed_party.png', game, plot=True)
    # 107, 364, 402, 403

    # home point 1
    # template_matcher.feature_matcher(window_frame, 'home_point_1.png', game, plot=True)

    # template_matcher.feature_matcher(window_frame, 'make_party.png', game, plot=True)

    # template_matcher.feature_matcher_match_found(window_frame, 'find_raid', ['raid_1.png'], game, plot=True)

    # template_matcher.feature_matcher(window_frame, 'leave_cave.png', game, plot=True)


def cave_enter_success(game):
    window_frame = frame_capture.capture_window_frame(game.x, game.y, game.x2, game.y2, im_show=False)
    ef = template_matcher.feature_matcher(window_frame, 'failed_party.png', game)
    if ef[0] is None:
        return True
    else:
        return False


def home_point_1(game):
    window_frame = frame_capture.capture_window_frame(game.x, game.y, game.x2, game.y2, im_show=False)
    tp = template_matcher.feature_matcher(window_frame, 'home_point_1.png', game)
    if tp[0] is not None:
        target_offset_x, target_offset_y = random_utils.random_point(
            tp[0] + game.x, tp[1] + game.y, tp[2] + game.x, tp[3] + game.y
        )
        move_mouse.random_mouse_move(target_offset_x, target_offset_y, rnd=400, duration=0.5)
        pyautogui.click()
        time.sleep(5)
        print('not implemented right home point yet')
        game.__setstate__(KILL_PROCESS)
    else:
        print('[E] cannot find home point!!!')
        game.__setstate__(KILL_PROCESS)
