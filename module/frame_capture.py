from PIL import ImageGrab
import numpy as np
import cv2


def capture_window_frame(x, y, width, height, im_show=False):
    # bbox specifies specific region (bbox= x,y,width,height *starts top-left)
    img = ImageGrab.grab(include_layered_windows=True, all_screens=True, bbox=(x, y, width, height))
    img_np = np.array(img)  # this is the array obtained from conversion
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    if im_show:
        cv2.imshow("RuneFrame", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return frame


def capture_window_frame_continuous(x, y, width, height, im_show=False):
    img = ImageGrab.grab(include_layered_windows=True, all_screens=True, bbox=(x, y, width, height))
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    if im_show:
        cv2.imshow("Continuous", frame)
        cv2.waitKey(1)
        cv2.destroyAllWindows()
    return frame
