import cv2
import time


class FrameGetter:
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
        """
        Get the next frame from the video if enough time has passed.
        :return: NumPy array representing the frame, or None if it's not time for a new frame
        """

        ret, frame = self.cap.read()
        if ret:
            return frame
        else:
            self.cap.release()
            self.cap = cv2.VideoCapture(self.video_path)

