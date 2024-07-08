from camera import Camera
from print_debug import millis
from display_image import Display
import cv2
from frame import Frame
from SliderWindow import SliderWindow
from video_reader import FrameGetter
print_string = ""

cam = Camera()
slider_window = SliderWindow("Slider", 0, 360)
time_stamp = millis()

use_video = True
if use_video:
    frame_getter = FrameGetter("video.avi")
while True:

    if use_video:
        numpy_image = frame_getter.get_frame()
    else:
        numpy_image = cam.get_frame()
    if numpy_image is None:
        continue

    frame = Frame(numpy_image, slider_window.get_slider_values(), 800, 2300)


    display1 = Display("Original")
    display1.display_image(frame.get_frame_hsv(), cv2.COLOR_HSV2BGR)
    display2 = Display("Min Color")
    display2.display_image(frame.display_min_color(), cv2.COLOR_HSV2BGR)
    display3 = Display("Max Color")
    display3.display_image(frame.display_max_color(), cv2.COLOR_HSV2BGR)
    display4 = Display("Monochrom")
    display4.display_image(frame.get_frame_monochrom())
    display4 = Display("Monochrom filtered 1")
    display4.display_image(frame.get_frame_filtered_1())
    #display4 = Display("Monochrom filtered 2")
    #display4.display_image(frame.get_frame_filtered_2())
    #display4 = Display("Monochrom filtered 3")
    #display4.display_image(frame.get_frame_filtered_3())
    display4 = Display("Rows")
    display4.display_image(frame.get_rows(), cv2.COLOR_HSV2BGR)
    #frame = frame.get_frame_filtered()
    #continue
    t = millis()
    tt = t
    if tt < time_stamp:
        tt += 1000
    if t != time_stamp:
        print(1000/(tt - time_stamp))
        time_stamp = t


