from camera import Camera
from print_debug import millis, get_time
from display_image import Display
import cv2
from frame import Frame
from SliderWindow import SliderWindow
from video_reader import FrameGetter
from Frontend import Frontend
from time import sleep



print_string = ""

cam = Camera()
slider_configs = [
    {"name": "Min Blau", "min": 0, "max": 255},
    {"name": "Max Blau", "min": 0, "max": 255},
    {"name": "Min Gruen", "min": 0, "max": 255},
    {"name": "Max Gruen", "min": 0, "max": 255},
    {"name": "Min Rot", "min": 0, "max": 255},
    {"name": "Max Rot", "min": 0, "max": 255},
    {"name": "Expected Lines", "min": 0, "max": 10},
    {"name": "Filter 1", "min": 0, "max": 20},
    {"name": "Filter 2", "min": 0, "max": 20},
    {"name": "Filter 3", "min": 0, "max": 1000},
    {"name": "Filter 4", "min": 0, "max": 1000}
]

slider_window = SliderWindow("Custom Sliders", slider_configs)
time_stamp = millis()

use_video = True
if use_video:
    frame_getter = FrameGetter(r"D:\Videos Burger Wback\video 10.avi")
frontend = Frontend()
numpy_image = None

while True:
    t = millis()
    if numpy_image is None or frontend.run_video:
        if use_video:
            numpy_image = frame_getter.get_frame()
        else:
            numpy_image = cam.get_frame()
        if numpy_image is None:
            continue

    frame = Frame(numpy_image, slider_window.get_slider_values(), 800, 2300)
    frontend.update_frame(frame)

    #display1 = Display("Original")
    #display1.display_image(frame.get_frame(with_rows=True, with_level=True))







