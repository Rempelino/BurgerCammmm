import _thread
import gxipy as gx
import cv2
import numpy as np
from queue import Queue
from datetime import datetime
from print_debug import print_time, commit_print

q = Queue(maxsize=1)

class Camera():
    latest_numpy_image = None


    def __init__(self):
        _thread.start_new_thread(self.live_image, ("live_image", 1, ))

    def get_frame(self):
        while self.latest_numpy_image is None:
            pass
        if self.latest_numpy_image is not None:
            temp = self.latest_numpy_image
            self.latest_numpy_image = None
            return temp
        else:
            return None

    def live_image(self,threadName, delay):
        print("livethread")
        device_manager = gx.DeviceManager()
        dev_num, dev_info_list = device_manager.update_device_list()
        if dev_num == 0:
            print("Number of enumerated devices is 0")
            return
        cam = device_manager.open_device_by_index(1)
        if cam.PixelColorFilter.is_implemented() is False:
            print("This sample does not support mono camera.")
            cam.close_device()
            return
        cam.TriggerMode.set(gx.GxSwitchEntry.OFF)
        cam.data_stream[0].set_acquisition_buffer_number(1)
        cam.stream_on()
        while True:

            commit_print()
            print_time("time for commit  print")

            raw_image = cam.data_stream[0].get_image()
            print_time("got raw image")

            RGB_image = raw_image.convert("RGB")
            print_time("created RGB image")

            numpy_image = RGB_image.get_numpy_array()
            print_time("created RGB image")

            while self.latest_numpy_image is not None:
                pass
            print_time("wait until frame is read")

            self.latest_numpy_image = numpy_image
            print_time("put numpy image into takeaway buffer")


        # stop data acquisition
        cam.stream_off()

        # close device
        cam.close_device()
        cv2.destroyAllWindows()