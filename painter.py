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

        self.color_box_height = int(self.canvas_height/10)
        self.color_box_width = int(self.canvas_width/(len(self.color_list)))

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

        # draw the color boxes at the bottom of image
        for i in range(len(self.color_list)):
            self.canvas = cv2.rectangle(
                self.canvas, (self.color_box_width*i, self.canvas_height),
                (self.color_box_width*(i+1),
                 self.canvas_height - self.color_box_height),
                self.color_list[i], -1)

        # refresh the drawing status
        self.is_drawing = False
        self.start_point = (-1, -1)
        self.end_point = (-1, -1)

    def select_color(self, color):
        self.color = color

    def zone(self, x, y):
        if 0 < x and x < self.canvas_width \
                and self.canvas_height-self.color_box_height < y and y < self.canvas_height:
            return "selecting"
        return "drawing"
