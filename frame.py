import cv2
import numpy
import numpy as np
from display_image import Display

Line_detection_threshold = 0


class Frame:
    global Line_detection_threshold
    frame_HSV = None
    frame_monochrom = None
    frame_filtered_1 = None
    frame_filtered_2 = None
    frame_filtered_3 = None
    lines = None


    red = np.array([np.uint8(0), np.uint8(255), np.uint8(255)])
    yellow = np.array([np.uint8(50), np.uint8(255), np.uint8(255)])
    white = np.array([np.uint8(0), np.uint8(0), np.uint8(255)])
    black = np.array([np.uint8(0), np.uint8(255), np.uint8(0)])

    resize = True
    def __init__(self, frame, param, y1, y2):

        self.frame_BGR = frame[y1:y2, :]

        if self.resize:
            height, width, _ = self.frame_BGR.shape
            self.frame_height = 300
            self.frame_width = int(self.frame_height / height * width)
            self.frame_BGR = cv2.resize(self.frame_BGR, (self.frame_width, self.frame_height))
        else:
            self.frame_height, self.frame_width, _ = self.frame_BGR.shape

        self.min_color = np.array([param[0], param[2], param[4]])
        self.max_color = np.array([param[1], param[3], param[5]])
        self.expected_lines = param[6]

        self.filter_constant = param[7:11]
        self.line_detection_threshold = Line_detection_threshold

        self.recursion_counter = 0

    def get_frame_hsv(self, with_rows=False, with_level=False):
        if self.frame_HSV is None:
            self.frame_HSV = cv2. cvtColor(self.frame_BGR, cv2.COLOR_BGR2HSV)
        new_frame = self.frame_HSV.copy()
        if with_rows:
            new_frame = self.add_line(new_frame)
        if with_level:
            new_frame = self.overlay_number(new_frame)
        return new_frame

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
            self.frame_monochrom = self.grayscale_to_hsv(cv2.inRange(self.get_frame_hsv(), self.min_color, self.max_color))
        return self.frame_monochrom

    def get_frame_filtered_1(self, with_rows=False):
        if self.frame_filtered_1 is not None:
            if with_rows:
                frame = self.add_line(self.frame_filtered_1)
                return frame
            return self.frame_filtered_1

        frame = self.hsv_to_grayscale(self.get_frame_filtered_2().copy())
        frame = self.remove_small_objects(frame, self.filter_constant[0])
        #frame = self.remove_object_below_height(frame, 30)
        frame = self.remove_small_objects(255 - frame, self.filter_constant[1])
        frame = 255 - frame
        frame = self.grayscale_to_hsv(frame)
        self.frame_filtered_1 = frame
        if with_rows:
            frame = self.add_line(frame)
        return frame

    def remove_small_objects(self, image, min_size):
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(image, connectivity=8)
        result = np.zeros_like(image)
        for label in range(1, num_labels):
            if stats[label, cv2.CC_STAT_AREA] >= min_size:
                result[labels == label] = 255
        return result

    def remove_object_below_height(self, image, min_height):
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(image, connectivity=8)
        result = np.zeros_like(image)
        for label in range(1, num_labels):
            if stats[label, cv2.CC_STAT_HEIGHT] >= min_height:
                result[labels == label] = 255
        return result


    def get_frame_filtered_2(self, with_rows=False):
        if self.frame_filtered_2 is not None:
            if with_rows:
                return self.add_line(self.frame_filtered_2)
            return self.frame_filtered_2

        frame = self.hsv_to_grayscale(self.get_frame_filtered_3().copy())
        frame[frame == 255] = 1
        output = np.zeros((self.frame_height, self.frame_width))
        for x in range(self.frame_width):
            is_white = 0
            count = 0
            for y in range(self.frame_height):
                if frame[y, x]:
                    count += 1
                elif not frame[y, x] and is_white:
                    if count > self.filter_constant[2]:
                        output[y - count:y, x] = 1
                    count = 0
                is_white = frame[y, x]
            if frame[self.frame_height-1, x]:
                if count > 10:
                    output[self.frame_height - count:self.frame_height, x] = 1

        new_frame = cv2.inRange(output, 1, 1)
        new_frame = self.grayscale_to_hsv(new_frame)
        self.frame_filtered_2 = new_frame
        if with_rows:
            new_frame = self.add_line(new_frame)
        return new_frame


    def get_frame_filtered_3(self):
        if self.frame_filtered_3 is not None:
            return self.frame_filtered_3

        frame = self.hsv_to_grayscale(self.get_frame_monochrom().copy())
        frame[frame == 255] = 1
        output = np.zeros((self.frame_height, self.frame_width))
        for y in range(self.frame_height):
            is_white = 0
            count = 0
            for x in range(self.frame_width):
                if frame[y, x]:
                    count += 1
                elif not frame[y, x] and is_white:
                    if count > self.filter_constant[3]:
                        output[y, x - count:x] = 1
                    count = 0
                is_white = frame[y, x]
            if frame[y, self.frame_width-1]:
                if count > 10:
                    output[y, self.frame_width - count:self.frame_width] = 1

        self.frame_filtered_3 = self.grayscale_to_hsv(cv2.inRange(output, 1, 1))
        return self.frame_filtered_3

    def get_frame_pixel_sums(self, with_rows=False):
        frame = self.hsv_to_grayscale(self.get_frame_filtered_1().copy())
        sum_of_pixels = np.sum(frame, 1)

        new_frame = np.zeros([self.frame_height, self.frame_width, 3], dtype=np.uint8)
        for index, pixel_row in enumerate(sum_of_pixels):
            quotient, _ = divmod(pixel_row, 255)
            new_frame[index, :quotient] = self.white

        if with_rows:
            new_frame = self.add_line(new_frame)
            new_frame = self.add_threshold(new_frame)
        return new_frame

    def add_line(self, frame):
        new_frame = frame.copy()
        for line in self.get_lines():
            new_line = np.zeros((5, self.frame_width, 3))
            new_line[:, :] = self.red
            y = line[0]
            start = max(0, y - 2)
            end = min(self.frame_height, y + 3)
            new_frame[start:end] = new_line[:end - start]
        return new_frame

    def get_lines(self):
        if self.lines is not None:
            return self.lines
        global Line_detection_threshold
        frame = self.hsv_to_grayscale(self.get_frame_filtered_1().copy())
        sum_of_pixels = np.sum(frame, 1)
        line_counter = 0
        lines = []
        for y in range(self.frame_height):
            if sum_of_pixels[y] > self.line_detection_threshold:
                line_counter += 1
            elif line_counter > 5:
                line_position = int(y - (line_counter / 2))
                line_value = sum_of_pixels[line_position]
                lines.append([line_position, line_value])
                line_counter = 0
        if len(lines) > self.expected_lines:
            Line_detection_threshold += 1000
            self.line_detection_threshold = Line_detection_threshold
        if len(lines) < self.expected_lines:
            Line_detection_threshold += 1000
            self.line_detection_threshold = Line_detection_threshold
        if Line_detection_threshold > self.frame_width * 255:
            Line_detection_threshold = 0
        if len(lines) == self.expected_lines or self.recursion_counter > 500:
            self.lines = lines
        else:
            self.recursion_counter += 1
            self.get_lines()

        return lines

    def add_threshold(self, frame):
        new_frame = frame.copy()
        new_frame[0:self.frame_height, int((self.line_detection_threshold/255)-2): int((self.line_detection_threshold/255) + 2)] = self.yellow
        return new_frame

    def grayscale_to_hsv(self, gray_image):
        if gray_image.dtype != np.uint8:
            gray_image = cv2.normalize(gray_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        gray_3d = cv2.merge([gray_image] * 3)
        bgr_image = gray_3d
        hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
        return hsv_image

    def hsv_to_grayscale(self, hsv_image):
        # Convert HSV to BGR
        bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

        # Convert BGR to grayscale
        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)

        return gray_image

    def overlay_number(self, frame):
        thickness = 2
        color = (255, 255, 255)
        font_scale = 1
        # Convert the number to string

        # Define the font
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Put the text on the image
        for line in self.get_lines():
            text = str(int(line[1]/255/50))
            cv2.putText(frame, text, [0, line[0]], font, font_scale, color, thickness, cv2.LINE_AA)

        return frame