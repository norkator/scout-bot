from module import template_matcher
import os


def start_app():
    input_image = os.getcwd() + '/images/' + 'beginning2.png'
    compass_template_image = os.getcwd() + '/images/' + 'compass.png'
    compass_points = template_matcher.find_matching_position(input_image, compass_template_image, ['cv.TM_SQDIFF_NORMED'])
    print(compass_points)


start_app()
