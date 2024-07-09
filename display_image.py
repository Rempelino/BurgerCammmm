import cv2
from queue import Queue


class Display:
    def __init__(self, window_name="Image"):
        self.q = Queue(maxsize=1)
        self.m_gLiveFlag = 1
        self.m_gProcessFlag = 1
        self.window_name = window_name

    def display_image(self, numpy_image, color=None):
        #default color coding is BGR

        if color is not None:
            pimg = cv2.cvtColor(numpy_image, color)
        else:
            pimg = numpy_image

        if self.q.qsize() == 0:
            self.q.put(pimg)
        if pimg.ndim == 3:
            height, width, _ = pimg.shape
        else:
            height, width = pimg.shape
        new_width = 900
        new_height = int(new_width / width * height)
        pimg = cv2.resize(pimg, (new_width, new_height))
        cv2.imshow(self.window_name, pimg)
        cv2.waitKey(10)
