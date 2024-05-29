import math
import pyxel
from . import core


class Lerp(core.BaseGameObject):

    def __init__(self, obj, start, end, speed=1, constant=True):
        self.constant = constant
        self.obj = obj
        self.start = start
        self.end = end
        self.progress = 0
        self.speed = speed
        self.distance = math.sqrt((self.end[0] - self.start[0])**2 + (self.end[1] - self.start[1])**2)
        self.ratio = self.distance / self.speed
        self.auto_play = True

    def update(self):
        x = self.start[0] + (self.end[0] - self.start[0]) * self.progress
        y = self.start[1] + (self.end[1] - self.start[1]) * self.progress
        self.obj.x = x
        self.obj.y = y
        if self.auto_play:
            if self.constant:
                self.progress += (self.speed * 0.1) / self.ratio
            else:
                self.progress += (self.speed * 0.1) * 0.01

    def draw(self):
        pass
