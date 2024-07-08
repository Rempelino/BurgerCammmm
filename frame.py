import cv2
import numpy
import numpy as np
from display_image import Display

class Frame:
    frame_HSV = None
    frame_monochrom = None
    frame_filtered_1 = None
    frame_filtered_2 = None
    frame_filtered_3 = None
    filter_constant = 1
    resize = True
    def __init__(self, frame, min_max, y1, y2):

        self.frame_BGR = frame[y1:y2, :]

        if self.resize:
            height, width, _ = self.frame_BGR.shape
            self.frame_height = 300
            self.frame_width = int(self.frame_height / height * width)
            self.frame_BGR = cv2.resize(self.frame_BGR, (self.frame_width, self.frame_height))
        else:
            self.frame_height, self.frame_width, _ = self.frame_BGR.shape

        self.min_color = np.array([min_max[0], 0, 0])
        self.max_color = np.array([min_max[1], 255, 255])

        self.field_size = 1 + 2 * self.filter_constant

    def get_frame_hsv(self):
        if self.frame_HSV is None:
            self.frame_HSV = cv2. cvtColor(self.frame_BGR, cv2.COLOR_BGR2HSV)
        return self.frame_HSV

    def display_max_color(self):
        new_frame = self.get_frame_hsv().copy()
        new_frame[:, :, 0] = self.max_color[0]
        return new_frame

    def display_min_color(self):
        new_frame = self.get_frame_hsv().copy()
        new_frame[:, :, 0] = self.min_color[0]
        return new_frame

    def get_frame_monochrom(self):

        if self.frame_monochrom is None:
            self.frame_monochrom = cv2.inRange(self.get_frame_hsv(), self.min_color, self.max_color)
        return self.frame_monochrom

        frame = np.empty((self.frame_height, self.frame_width))
        print(self.frame_height)
        frame[240:244, 800:804] = 255
        self.frame_monochrom = frame
        return frame

    def get_frame_filtered_1(self):
        if self.frame_filtered_1 is not None:
            return self.frame_filtered_1

        frame = self.get_frame_monochrom().copy()
        frame = self.remove_small_objects(frame, 100)
        frame = self.remove_small_objects(255 - frame, 100)
        frame = 255 - frame
        self.frame_filtered_1 = frame
        return frame

    def remove_small_objects(self, image, min_size):
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(image, connectivity=8)
        result = np.zeros_like(image)
        for label in range(1, num_labels):
            if stats[label, cv2.CC_STAT_AREA] >= min_size:
                result[labels == label] = 255
        return result


    def get_frame_filtered_2(self):
        if self.frame_filtered_2 is not None:
            return self.frame_filtered_2

        frame = self.get_frame_filtered_1().copy()
        frame[frame == 255] = 1
        output = np.zeros((self.frame_height, self.frame_width))
        for x in range(self.frame_width):
            is_white = 0
            count = 0
            for y in range(self.frame_height):
                if frame[y, x]:
                    count += 1
                elif not frame[y, x] and is_white:
                    if count > 10:
                        output[y - count:y, x] = 1
                    count = 0
                is_white = frame[y, x]
            if frame[self.frame_height-1, x]:
                if count > 10:
                    output[self.frame_height - count:self.frame_height, x] = 1
        self.frame_filtered_2 = cv2.inRange(output, 1, 1)
        return self.frame_filtered_2

    def get_frame_filtered_3(self):
        if self.frame_filtered_3 is not None:
            return self.frame_filtered_3

        frame = self.get_frame_filtered_2().copy()
        frame[frame == 255] = 1
        output = np.zeros((self.frame_height, self.frame_width))
        display = Display("temp")
        for y in range(self.frame_height):
            is_white = 0
            count = 0
            for x in range(self.frame_width):
                if frame[y, x]:
                    count += 1
                elif not frame[y, x] and is_white:
                    if count > 10:
                        output[y, x - count:x] = 1
                        #temp = output * 125
                        #display.display_image(temp)
                    count = 0
                is_white = frame[y, x]
            if frame[y, self.frame_width-1]:
                if count > 10:
                    output[y, self.frame_width - count:self.frame_width] = 1


        self.frame_filtered_3 = cv2.inRange(output, 1, 1)
        return self.frame_filtered_3

    def get_rows(self):
        expected_lines = 6
        frame = self.get_frame_filtered_1().copy()
        sum_of_pixels = np.sum(frame, 1)
        line_counter = 0
        lines = []
        for y in range(self.frame_height):
            if sum_of_pixels[y] > 50000:
                line_counter += 1
            elif line_counter > 5:
                line_position = int(y - (line_counter / 2))
                line_value = sum_of_pixels[line_position]
                lines.append([line_position, line_value])
                line_counter = 0

        frame = self.get_frame_hsv().copy()
        for line in lines:
            new_line = np.zeros((5, self.frame_width,3))
            red = np.array([0, 255, 255])
            new_line[:, :] = red
            y = line[0]
            start = max(0, y - 2)
            end = min(self.frame_height, y + 3)
            frame[start:end] = new_line[:end - start]

        return frame









        return sum_of_pixels


