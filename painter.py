import cv2
import numpy as np


class Painter:
    def __init__(self, canvas_height, canvas_width):
        # size of canvas
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width

        # color list and current selected color
        self.color = 0
        self.color_list = [
            (255, 255, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 255)
        ]

        # refresh canvas
        self.refresh_canvas(self.canvas_height, self.canvas_width)

    def start_draw(self, start_point):
        self.is_drawing = True
        if self.start_point == (-1, -1):
            self.start_point = start_point

    def draw(self, point):
        if self.is_drawing:
            self.end_point = point
            cv2.line(self.canvas, self.start_point,
                     self.end_point, self.color_list[self.color], 2)
            self.start_point = self.end_point

    def end_draw(self):
        self.is_drawing = False
        self.start_point = (-1, -1)

    def refresh_canvas(self, canvas_height, canvas_width):
        # refresh the canvas
        self.canvas = np.zeros(
            (canvas_height, canvas_width, 3), np.uint8)
        '''self.canvas = cv2.rectangle(
            self.canvas, (0, 0), (160, 50), self.color_list[0], -1)
        self.canvas = cv2.rectangle(
            self.canvas, (160, 0), (320, 50), self.color_list[1], -1)
        self.canvas = cv2.rectangle(
            self.canvas, (320, 0), (480, 50), self.color_list[2], -1)
        self.canvas = cv2.rectangle(
            self.canvas, (480, 0), (640, 50), self.color_list[3], -1)'''

        l = len(self.color_list)
        for i in range(l):
            a = int(i*self.canvas_width/len(self.color_list))
            b = int((i+1)*self.canvas_width/len(self.color_list))
            self.canvas = cv2.rectangle(
                self.canvas, (a, 0), (b, 50), self.color_list[i], -1)

        # refresh the drawing status
        self.is_drawing = False
        self.start_point = (-1, -1)
        self.end_point = (-1, -1)

    def select_color(self, color):
        self.color = color
