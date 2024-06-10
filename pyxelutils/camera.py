import pyxel
from . import core


class FollowCamera(core.BaseGameObject):
    def __init__(self, target, bounds, smooth_speed=0.3):
        self.target = target
        self.bounds = bounds
        self.x = 0
        self.y = 0
        self.x_end = 0
        self.y_end = 0
        self.offset_x = core.BaseGame.instance.w // 2 - target.action.current.w // 2
        self.offset_y = core.BaseGame.instance.h // 2 - target.action.current.h // 2
        self.lerp_speed = smooth_speed

    def update(self):
        pyxel.camera()
        x = self.target.x - self.offset_x
        y = self.target.y - self.offset_y

        self.x += (x - self.x) * self.lerp_speed
        self.y += (y - self.y) * self.lerp_speed

        self.x = max(self.bounds[0][0], min(self.x, self.bounds[1][0] - core.BaseGame.instance.w))
        self.y = max(self.bounds[0][1], min(self.y, self.bounds[1][1] - core.BaseGame.instance.h))

        pyxel.camera(self.x, self.y)

    def draw(self):
        pass

