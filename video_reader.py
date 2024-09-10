import cv2
import time


class FrameGetter:
    last_frame = None
    frame_counter = 0
    def __init__(self, video_path):
        """
        Initialize the FrameGetter.
        :param video_path: String path to the video file
        """
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise ValueError("Error: Couldn't open the video file.")

    def get_frame(self):
        ret, frame = self.cap.read()
        if ret:
            self.last_frame = frame
            return self.last_frame
        else:
            self.cap.release()
            self.cap = cv2.VideoCapture(self.video_path)
            return self.last_frame

