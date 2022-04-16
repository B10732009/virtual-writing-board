import time


class FPS:
    def __init__(self):
        # initialize all values
        self.previous_time = 0
        self.current_time = 0
        self.fps = 0

    def refresh(self):
        # get time elasped from the beginning of program
        self.current_time = time.time()

        # calculate the FPS
        self.fps = (int)(1/(self.current_time - self.previous_time))

        # set current time to previos time
        self.previous_time = self.current_time

    def get_fps(self):
        return self.fps
