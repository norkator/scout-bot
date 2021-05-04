from matplotlib import pyplot as plt
import cv2 as cv
import os

'''
    # methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
    # 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
'''

MIN_MATCH_QUALITY = 0.9


# use template matching to find something from image
def find_matching_position(input_image, to_find_image, matcher_method, plot=False, im_show=False):
    img2 = input_image
    template = cv.imread(to_find_image, 0)
    w, h = template.shape[::-1]
    img = img2.copy()
    method = eval(matcher_method)
    # Apply template Matching
    res = cv.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    if max_val > MIN_MATCH_QUALITY:
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv.rectangle(img, top_left, bottom_right, 255, 2)
        if plot:
            plt.subplot(121), plt.imshow(res, cmap='gray')
            plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
            plt.subplot(122), plt.imshow(img, cmap='gray')
            plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
            plt.suptitle(matcher_method)
            plt.show()
        if im_show:
            window_name = "Matcher"
            cv.moveWindow(window_name, 1430, 65)
            cv.imshow(window_name, img)
            cv.waitKey(1)  # no freeze, refreshes for a millisecond

        return [min_loc[0], min_loc[1], (top_left[0] + w), (top_left[1] + h)]
    else:
        return [None, None, None, None]


def feature_matcher(input_image, match_image, plot=True, im_show=False):
    compass_template_image = os.getcwd() + '/images/' + match_image
    target_point = find_matching_position(
        input_image, compass_template_image, 'cv.TM_CCOEFF_NORMED', plot=plot, im_show=im_show
    )
    print('target point frame: ' + str(target_point))
    return target_point
