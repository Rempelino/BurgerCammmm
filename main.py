from camera import Camera
from print_debug import millis, get_time
from display_image import Display
import cv2
from frame import Frame
from SliderWindow import SliderWindow
from video_reader import FrameGetter
print_string = ""

cam = Camera()
slider_configs = [
    {"name": "Min Farbwert", "min": 0, "max": 179},
    {"name": "Max Farbwert", "min": 0, "max": 179},
    {"name": "Min Saettigung", "min": 0, "max": 255},
    {"name": "Max Saettigung", "min": 0, "max": 255},
    {"name": "Min Helligkeit", "min": 0, "max": 255},
    {"name": "Max Helligkeit", "min": 0, "max": 255},
    {"name": "Expected Lines", "min": 0, "max": 10},
    {"name": "Filter 1", "min": 0, "max": 1000},
    {"name": "Filter 2", "min": 0, "max": 1000},
    {"name": "Filter 3", "min": 0, "max": 20},
    {"name": "Filter 4", "min": 0, "max": 20}
]
slider_window = SliderWindow("Custom Sliders", slider_configs)


time_stamp = millis()

use_video = True
if use_video:
    frame_getter = FrameGetter(r"D:\Videos Burger Wback\video 10.avi")
numpy_image = None
while True:
    t = millis()
    if numpy_image is None or True:
        if use_video:
            numpy_image = frame_getter.get_frame()
        else:
            numpy_image = cam.get_frame()
        if numpy_image is None:
            continue
    frame = Frame(numpy_image, slider_window.get_slider_values(), 800, 2300)
    display1 = Display("Original")
    display1.display_image(frame.get_frame_hsv())#with_rows=True, with_level=True))
    print(f'this took {get_time()} milliseconds')
    continue
    display2 = Display("Min Color")
    display2.display_image(frame.display_min_color())
    display3 = Display("Max Color")
    display3.display_image(frame.display_max_color())
    display4 = Display("Monochrom")
    display4.display_image(frame.get_frame_monochrom())
    display4 = Display("Monochrom filtered 1")
    display4.display_image(frame.get_frame_filtered_1())
    display4 = Display("Monochrom filtered 2")
    display4.display_image(frame.get_frame_filtered_2())
    display4 = Display("Monochrom filtered 3")
    display4.display_image(frame.get_frame_filtered_3())
    display4 = Display("Pixel Summen")
    display4.display_image(frame.get_frame_pixel_sums(with_rows=True))



    print(f'this took {get_time()} milliseconds')


