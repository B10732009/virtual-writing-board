import time


class FPS:
    def __init__(self):
        self.previous_time = 0
        self.current_time = 0
        self.fps = 0

    def refresh(self):
        self.current_time = time.time()
        self.fps = (int)(1/(self.current_time - self.previous_time))
        self.previous_time = self.current_time

    def get_fps(self):
        return self.fps
