from module import config_parser, template_matcher, frame_capture, move_mouse
import pyautogui
import os


def start_app():
    games = config_parser.get_games()
    for game in games:

        # window frame capture
        window_frame = frame_capture.capture_window_frame(game.x, game.y, game.x2, game.y2, im_show=False)
        
        # compass detection
        input_image = window_frame  # input_image = os.getcwd() + '/images/' + 'beginning2.png'
        compass_template_image = os.getcwd() + '/images/' + 'compass.png'
        compass_points = template_matcher.find_matching_position(
            input_image, compass_template_image, ['cv.TM_SQDIFF_NORMED'], plot=True
        )
        print('compass point frame: ' + str(compass_points))
        
        # move mouse
        move_mouse.random_mouse_move(compass_points[0], compass_points[1], rnd=400, duration=1.0)
        # pyautogui.moveTo(compass_points[0] + 20, compass_points[1] + 100, 4)


start_app()
