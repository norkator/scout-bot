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
STATE_CAVE_FINISHED = 12
KILL_PROCESS = 666


def scout(game):
    # window frame capture
    window_frame = frame_capture.capture_window_frame(game.x, game.y, game.x2, game.y2, im_show=False)

    if game.is_sleeping() is False:
        if game.get_state() is STATE_BEGINNING:
            tp = template_matcher.feature_matcher(window_frame, 'compass.png', game)
            if tp[0] is None:
                game.__setstate__(STATE_BEGINNING)
                play_sound('wpn_select.wav')
            else:
                target_offset_x, target_offset_y = random_utils.random_point(
                    tp[0] + game.x, tp[1] + game.y, tp[2] + game.x, tp[3] + game.y
                )
                move_mouse.random_mouse_move(target_offset_x, target_offset_y, rnd=400, duration=0.5)
                pyautogui.click()
                game.__setstate__(STATE_CLICK_BOARD)

        elif game.get_state() is STATE_CLICK_BOARD:
            tp = template_matcher.feature_matcher(window_frame, 'board_2.png', game)
            if tp[0] is None:
                tp = template_matcher.feature_matcher(window_frame, 'board.png', game)  # try with another board image
            if tp[0] is not None:
                target_offset_x, target_offset_y = random_utils.random_point(
                    tp[0] + game.x, tp[1] + game.y, tp[2] + game.x, tp[3] + game.y
                )
                move_mouse.random_mouse_move(target_offset_x, target_offset_y, rnd=400, duration=0.5)
                pyautogui.click()
                game.__setstate__(STATE_MAKE_PARTY)
                game.set_sleep(4)
            else:
                find_starting_point(game)

        elif game.get_state() is STATE_MAKE_PARTY:
            tp = template_matcher.feature_matcher(window_frame, 'make_party.png', game)
            if tp[0] is not None:
                target_offset_x, target_offset_y = random_utils.random_point(
                    tp[0] + game.x, tp[1] + game.y, tp[2] + game.x, tp[3] + game.y
                )
                move_mouse.random_mouse_move(target_offset_x, target_offset_y, rnd=400, duration=0.5)
                pyautogui.click()
                game.__setstate__(STATE_CAVE_MARKER)
                game.set_sleep(1)
            else:
                find_starting_point(game)

        elif game.get_state() is STATE_CAVE_MARKER:
            tp = template_matcher.feature_matcher(window_frame, 'target_point.png', game)
            target_offset_x, target_offset_y = random_utils.random_point(
                tp[0] + game.x, tp[1] + game.y, tp[2] + game.x, tp[3] + game.y
            )
            move_mouse.random_mouse_move(target_offset_x, target_offset_y, rnd=400, duration=0.5)
            pyautogui.click()
            game.__setstate__(STATE_ENTER_CAVE)
            game.set_sleep(8)

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
            game.set_sleep(4)

        elif game.get_state() is STATE_CAVE_DETECT_OPTIMAL_RAID:
            if is_bad_raid(window_frame, game):
                game.__setstate__(STATE_CAVE_EXIT)
            else:
                game.__setstate__(STATE_CAVE_ALARM)
                open_raid_reloader(game)

        elif game.get_state() is STATE_CAVE_EXIT:
            click_exit_cave(game=game, x_p=60, y_p=80)
            window_frame = frame_capture.capture_window_frame(game.x, game.y, game.x2, game.y2, im_show=False)
            tp = template_matcher.feature_matcher(window_frame, 'leave_cave.png', game)
            if tp[0] is None:
                click_exit_cave(game=game, x_p=80, y_p=80)  # try with another point
                window_frame = frame_capture.capture_window_frame(game.x, game.y, game.x2, game.y2, im_show=False)
                tp = template_matcher.feature_matcher(window_frame, 'leave_cave.png', game)
            target_offset_x, target_offset_y = random_utils.random_point(
                tp[0] + game.x, tp[1] + game.y, tp[2] + game.x, tp[3] + game.y
            )
            move_mouse.random_mouse_move(target_offset_x, target_offset_y, rnd=400, duration=0.5)
            pyautogui.click()
            print('[' + game.get_game_name() + '][' + str(game.get_state()) + '] exiting cave')
            game.__setstate__(STATE_BEGINNING)
            game.set_sleep(5)

        elif game.get_state() is STATE_CAVE_ALARM:
            play_sound('bell.wav')
            play_sound('bell.wav')
            play_sound('bell.wav')
            play_sound('alert.wav')
            game.__setstate__(STATE_CAVE_FINISHED)

        elif game.get_state() is STATE_CAVE_FINISHED:
            print('[' + game.get_game_name() + '] this window is in finished state (requiring reset)')
            # Todo, maybe ad key to reset this?

        elif game.get_state() is KILL_PROCESS:
            sys.exit(0)


# test scout vie finding specific object
def scout_test(game):
    # window frame capture
    window_frame = frame_capture.capture_window_frame(game.x, game.y, game.x2, game.y2, im_show=False)
    # move_mouse.random_mouse_move(game.x, game.y, rnd=400, duration=0.5)
    # print(is_bad_raid(window_frame, game))
    # click_exit_cave(game=game, x_p=60, y_p=80)
    # template_matcher.feature_matcher(window_frame, 'bad_raid.png', game, min_match_quality=0.3, plot=True)
    # template_matcher.feature_matcher(window_frame, 'raid_reload_toggle.png', game, min_match_quality=0.6, plot=True)
    # template_matcher.feature_matcher(window_frame, 'reload_raid.png', game, min_match_quality=0.4, plot=True)
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
    # template_matcher.feature_matcher_match_found(window_frame, 'find_raid', ['raid__1.png'], game, plot=True)
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
        time.sleep(8)
        find_starting_point(game)
    else:
        print('[E] cannot find home point!!!')
        game.__setstate__(STATE_CAVE_FINISHED)


def find_starting_point(game):
    print('[' + game.get_game_name() + '][' + str(game.get_state()) + '] trying to find starting point!')
    window_frame = frame_capture.capture_window_frame(game.x, game.y, game.x2, game.y2, im_show=False)
    tp = template_matcher.feature_matcher(window_frame, 'starting_point.png', game)
    play_sound('blip1.wav')
    if tp[0] is not None:
        target_offset_x, target_offset_y = random_utils.random_point(
            tp[0] + game.x, tp[1] + game.y, tp[2] + game.x, tp[3] + game.y
        )
        move_mouse.random_mouse_move(target_offset_x, target_offset_y, rnd=300, duration=0.2)
        pyautogui.click()
        time.sleep(2)
        game.__setstate__(STATE_BEGINNING)
    else:
        game.__setstate__(STATE_BEGINNING)


def is_bad_raid(window_frame, game):
    tp = template_matcher.feature_matcher(window_frame, 'bad_raid.png', game, min_match_quality=0.4, plot=False)
    return False if tp[0] is None else True  # does not find bad raid


def play_sound(sound_name):
    alert = os.getcwd() + '/sounds/' + sound_name
    playsound(alert)


# this tries to calculate position to leave cave
def click_exit_cave(game, x_p, y_p):
    x_p = int(((game.x2 / 2) + game.x) * x_p / 100)
    y_p = int(((game.y2 / 2) + game.y) * y_p / 100)
    move_mouse.random_mouse_move(x_p, y_p, rnd=400, duration=0.5)
    pyautogui.click()
    time.sleep(2)


def open_raid_reloader(game):
    window_frame = frame_capture.capture_window_frame(game.x, game.y, game.x2, game.y2, im_show=False)
    tp = template_matcher.feature_matcher(window_frame, 'raid_reload_toggle.png',
                                          game, min_match_quality=0.6, plot=False)
    if tp[0] is not None:
        target_offset_x, target_offset_y = random_utils.random_point(
            tp[0] + game.x, tp[1] + game.y, tp[2] + game.x, tp[3] + game.y
        )
        move_mouse.random_mouse_move(target_offset_x, target_offset_y, rnd=300, duration=0.5)
        pyautogui.click()
        print('[' + game.get_game_name() + '][' + str(game.get_state()) + '] open raid reloader')
        time.sleep(1)
        reload_raid(game)
    else:
        print('[' + game.get_game_name() + '][' + str(game.get_state()) + '] failed to open reload raid!')


def close_raid_reloader(game):
    w2 = 280  # 280 pixels more on x2
    window_frame = frame_capture.capture_window_frame(game.x, game.y, game.x2 + w2, game.y2, im_show=False)
    tp = template_matcher.feature_matcher(window_frame, 'raid_reload_toggle.png',
                                          game, min_match_quality=0.6, plot=False)
    if tp[0] is not None:
        target_offset_x, target_offset_y = random_utils.random_point(
            tp[0] + game.x, tp[1] + game.y, tp[2] + game.x, tp[3] + game.y
        )
        move_mouse.random_mouse_move(target_offset_x, target_offset_y, rnd=300, duration=0.5)
        pyautogui.click()
        print('[' + game.get_game_name() + '][' + str(game.get_state()) + '] close raid reloader')


def reload_raid(game):
    w2 = 280  # 280 pixels more on x2
    window_frame = frame_capture.capture_window_frame(game.x, game.y, game.x2 + w2, game.y2, im_show=False)
    tp = template_matcher.feature_matcher(window_frame, 'reload_raid.png',
                                          game, min_match_quality=0.6, plot=False)
    if tp[0] is not None:
        target_offset_x, target_offset_y = random_utils.random_point(
            tp[0] + game.x, tp[1] + game.y, tp[2] + game.x, tp[3] + game.y
        )
        move_mouse.random_mouse_move(target_offset_x, target_offset_y, rnd=250, duration=0.2)
        pyautogui.click()
        print('[' + game.get_game_name() + '][' + str(game.get_state()) + '] click raid reloader button')
        time.sleep(3)
        close_raid_reloader(game)
        time.sleep(1)
        window_frame = frame_capture.capture_window_frame(game.x, game.y, game.x2 + w2, game.y2, im_show=False)
        if is_bad_raid(window_frame, game):
            game.__setstate__(STATE_CAVE_EXIT)
        else:
            game.__setstate__(STATE_CAVE_ALARM)
    else:
        print('[' + game.get_game_name() + '][' + str(game.get_state()) + '] failed to reload raid!')
