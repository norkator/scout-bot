from module import template_matcher, frame_capture, move_mouse, random_utils
import pyautogui
import os

# scout states
STATE_BEGINNING = 0
STATE_CLICK_BOARD = 1
STATE_MAKE_PARTY = 2


def scout(game):
    # window frame capture
    window_frame = frame_capture.capture_window_frame(game.x, game.y, game.x2, game.y2, im_show=False)

    if game.get_state() is STATE_BEGINNING:
        # compass detection
        tp = feature_matcher(window_frame, 'compass.png')

        # get randomised clicking point
        target_offset_x, target_offset_y = random_utils.random_point(
            tp[0] + game.x, tp[1] + game.y, tp[2] + game.x, tp[3] + game.y
        )

        # move mouse
        move_mouse.random_mouse_move(target_offset_x, target_offset_y, rnd=400, duration=0.5)
        pyautogui.click()  # pyautogui.moveTo(compass_points[0] + 20, compass_points[1] + 100, 4)

        game.__setstate__(STATE_CLICK_BOARD)

    elif game.get_state() is STATE_CLICK_BOARD:
        tp = feature_matcher(window_frame, 'board.png')

        # get randomised clicking point
        target_offset_x, target_offset_y = random_utils.random_point(
            tp[0] + game.x, tp[1] + game.y, tp[2] + game.x, tp[3] + game.y
        )

        # move mouse
        move_mouse.random_mouse_move(target_offset_x, target_offset_y, rnd=400, duration=0.5)
        pyautogui.click()

        game.__setstate__(STATE_BEGINNING)


def feature_matcher(input_image, match_image):
    # input_image = os.getcwd() + '/images/' + 'beginning2.png'
    compass_template_image = os.getcwd() + '/images/' + match_image
    target_point = template_matcher.find_matching_position(
        input_image, compass_template_image, ['cv.TM_SQDIFF_NORMED'], plot=False
    )
    print('target point frame: ' + str(target_point))
    return target_point
