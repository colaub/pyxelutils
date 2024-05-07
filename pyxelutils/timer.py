import pyxel
from . import core


class Timer(core.BaseGameObject):
    def __init__(self, fps=30):
        self.is_running = False
        self.start_frame = 0
        self.stop_frame = 0
        self.elapsed_frames = 0
        self.fps = fps

    def start(self):
        if not self.is_running:
            self.start_frame = pyxel.frame_count
            self.is_running = True

    def stop(self):
        if self.is_running:
            self.stop_frame = pyxel.frame_count
            self.elapsed_frames += self.stop_frame - self.start_frame
            self.is_running = False

    def update(self):
        if self.is_running:
            self.elapsed_frames = pyxel.frame_count - self.start_frame

    def draw(self):
        pass

    @property
    def elapsed_time(self):
        return self.elapsed_frames * (self.fps * 0.001)
