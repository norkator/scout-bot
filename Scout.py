from module import template_matcher, frame_capture
import pyautogui
import os


def start_app():
    # window frame capture
    window_frame = frame_capture.capture_window_frame(0, 80, 1100, 700, im_show=False)

    # compass detection
    input_image = window_frame  # input_image = os.getcwd() + '/images/' + 'beginning2.png'
    compass_template_image = os.getcwd() + '/images/' + 'compass.png'
    compass_points = template_matcher.find_matching_position(
        input_image, compass_template_image, ['cv.TM_SQDIFF_NORMED'], plot=True
    )
    print('compass point frame: ' + str(compass_points))

    # move mouse
    pyautogui.moveTo(compass_points[0] + 20, compass_points[1] + 100, 4)


start_app()
