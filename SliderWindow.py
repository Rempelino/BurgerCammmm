import cv2
import numpy as np
import os

class SliderWindow:
    def __init__(self, window_name, slider_configs):
        self.window_name = window_name
        self.slider_file = f"{window_name}_slider_values.txt"
        self.is_running = True

        cv2.namedWindow(self.window_name)
        cv2.resizeWindow(self.window_name, 800, 600)

        self.slider_configs = slider_configs
        self.current_values = self.load_slider_values()

        # Ensure current_values has the correct length
        if len(self.current_values) < len(slider_configs):
            self.current_values.extend([config['min'] for config in slider_configs[len(self.current_values):]])
        elif len(self.current_values) > len(slider_configs):
            self.current_values = self.current_values[:len(slider_configs)]

        self.save_slider_values()

        for i, config in enumerate(slider_configs):
            short_name = config['name'][:3] + config['name'].split()[-1][:3]
            cv2.createTrackbar(short_name, self.window_name,
                               self.current_values[i] - config['min'], config['max'] - config['min'],
                               lambda value, index=i: self.on_slider_change(value, index))

        # Create toggle "button" using a trackbar
        cv2.createTrackbar("Toggle", self.window_name, 1, 1, self.toggle_button_callback)

    def on_slider_change(self, value, index):
        # Adjust the value to the actual range
        actual_value = value + self.slider_configs[index]['min']
        self.current_values[index] = actual_value
        print(f"Slider {index} changed to {actual_value}")
        self.save_slider_values()

    def get_slider_values(self):
        return self.current_values

    def load_slider_values(self):
        if os.path.exists(self.slider_file):
            with open(self.slider_file, 'r') as file:
                return [int(line.strip()) for line in file]
        else:
            return [config['min'] for config in self.slider_configs]

    def save_slider_values(self):
        with open(self.slider_file, 'w') as file:
            for value in self.current_values:
                file.write(f"{value}\n")

    def toggle_button_callback(self, state):
        self.is_running = bool(state)
        status = "Running" if self.is_running else "Stopped"
        print(f"Video {status}")

    def is_video_running(self):
        return self.is_running

    def __del__(self):
        self.save_slider_values()