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

        # set the size of color boxes
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

            if self.color == len(self.color_list)-1:
                cv2.line(self.canvas, self.start_point,
                         self.end_point, self.color_list[self.color], 40)
                self.refresh_tool_box()
            else:
                cv2.line(self.canvas, self.start_point,
                         self.end_point, self.color_list[self.color], 2)

            self.start_point = self.end_point

    def end_draw(self):
        self.is_drawing = False
        self.start_point = (-1, -1)

    def refresh_canvas(self, canvas_height, canvas_width):
        # reset canvas and tool box
        self.canvas = np.zeros(
            (canvas_height, canvas_width, 3), np.uint8)
        self.refresh_tool_box()

        # refresh the drawing status
        self.is_drawing = False
        self.start_point = (-1, -1)
        self.end_point = (-1, -1)

    def refresh_tool_box(self):
        # draw the color boxes at the bottom of image
        for i in range(len(self.color_list)-1):
            p1 = (self.color_box_width*i, self.canvas_height)
            p2 = (self.color_box_width*(i+1),
                  self.canvas_height - self.color_box_height)
            self.canvas = cv2.rectangle(
                self.canvas, p1, p2, self.color_list[i], -1)

        # load trash can and eraser pictures
        self.load_img('img/trash_can.png', 0, 0)
        self.load_img('img/eraser.png', self.canvas_height -
                      self.color_box_height, self.canvas_width - self.color_box_width)

    def load_img(self, filename, x, y):
        img = cv2.imread(filename)
        h, w, _ = img.shape
        self.canvas[x:x+h, y:y+w, :] = img[0:h, 0:w, :]

    def select_color(self, color):
        self.color = color

    def zone(self, x, y):
        if 0 < x and \
                x < self.canvas_width and \
                self.canvas_height-self.color_box_height < y and \
                y < self.canvas_height:
            return "selecting"
        elif 0 < x and x < 40 \
                and 0 < y and y < 40:
            return "cleaning"
        return "drawing"
