import cv2 as cv
from matplotlib import pyplot as plt


# use template matching to find something from image
def find_matching_position(input_image, to_find_image, methods, plot=False):
    # methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
    # 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
    # img = cv.imread(input_image, 0)
    img2 = input_image
    template = cv.imread(to_find_image, 0)
    w, h = template.shape[::-1]
    a = None
    b = None
    c = None
    d = None
    # All the 6 methods for comparison in a list
    for meth in methods:
        img = img2.copy()
        method = eval(meth)
        # Apply template Matching
        res = cv.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
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
            plt.suptitle(meth)
            plt.show()
        window_name = "Matcher"
        cv.moveWindow(window_name, 1430, 65)
        cv.imshow(window_name, img)
        cv.waitKey(1)  # no freeze, refreshes for a millisecond
        a = min_loc[0]
        b = min_loc[1]
        c = top_left[0] + w
        d = top_left[1] + h
        # print([min_loc[0], min_loc[1], top_left[0] + w, top_left[1] + h])
    return [a, b, c, d]
