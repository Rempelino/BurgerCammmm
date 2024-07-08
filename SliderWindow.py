import cv2
import numpy as np

class SliderWindow:
    def __init__(self, window_name, min_value, max_value):
        self.window_name = window_name
        self.min_value = min_value
        self.max_value = max_value
        self.current_value_slider_1 = 0
        self.current_value_slider_2 = 17

        # Create window
        cv2.namedWindow(self.window_name)

        # Create sliders
        cv2.createTrackbar("Slider 1", self.window_name, self.current_value_slider_1, max_value, self.on_slider1_change)
        cv2.createTrackbar("Slider 2", self.window_name, self.current_value_slider_2, max_value, self.on_slider2_change)

    def on_slider1_change(self, value):
        self.current_value_slider_1 = value

    def on_slider2_change(self, value):
        self.current_value_slider_1 = value

    def get_slider_values(self):
        slider1_value = cv2.getTrackbarPos("Slider 1", self.window_name)
        slider2_value = cv2.getTrackbarPos("Slider 2", self.window_name)
        return slider1_value, slider2_value

    def update(self):
        # This method keeps the window open and responsive
        cv2.waitKey(1)
