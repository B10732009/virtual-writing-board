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
            (255, 255, 255),
            (255, 128, 0),
            (255, 255, 0),
            (0, 255, 0),
            (0, 128, 255),
            (0, 0, 255),
            (128, 0, 255),
            (0, 0, 0)
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

            thickness = 2
            if self.color == len(self.color_list)-1:
                thickness = 40
            cv2.line(self.canvas, self.start_point,
                     self.end_point, self.color_list[self.color], thickness)

            self.start_point = self.end_point

    def end_draw(self):
        self.is_drawing = False
        self.start_point = (-1, -1)

    def refresh_canvas(self, canvas_height, canvas_width):
        # refresh the canvas
        self.canvas = np.zeros(
            (canvas_height, canvas_width, 3), np.uint8)
        self.refresh_tool_box()

        # refresh the drawing status
        self.is_drawing = False
        self.start_point = (-1, -1)
        self.end_point = (-1, -1)

    def refresh_tool_box(self):
        # draw the color boxes at the bottom of image
        for i in range(len(self.color_list)):
            p1 = (self.color_box_width*i, self.canvas_height)
            p2 = (self.color_box_width*(i+1),
                  self.canvas_height - self.color_box_height)
            '''if i == self.color:
                p2 = (self.color_box_width*(i+1),
                      self.canvas_height - self.color_box_height - 10)'''

            self.canvas = cv2.rectangle(
                self.canvas, p1, p2, self.color_list[i], -1)

        self.canvas = cv2.rectangle(
            self.canvas, (0, 0),
            (int(self.color_box_width/2), self.color_box_height),
            (255, 255, 255), -1)

    def select_color(self, color):
        self.color = color
        self.refresh_tool_box()

    def zone(self, x, y):
        if 0 < x and x < self.canvas_width \
                and self.canvas_height-self.color_box_height < y and y < self.canvas_height:
            return "selecting"
        elif 0 < x and x < int(self.color_box_width/2) \
                and 0 < y and y < self.color_box_height:
            return "cleaning"
        return "drawing"
